from django.contrib.auth import authenticate
from rest_framework import viewsets, status, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Image
from .serializers import UserSerializer, RegisterSerializer, ImageSerializer, LoginSerializer
from rest_framework.decorators import action

class RegisterAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['token'] = {
           'access_token': str(token.access_token),
           'refresh_token': str(token.refresh_token)
        }
        return Response(data, status=status.HTTP_201_CREATED)

class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['token'] = {
            'access_token': str(token.access_token),
            'refresh_token': str(token.refresh_token)
        }
        return Response(data, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh = request.data['refresh']
            token = RefreshToken.for_user(refresh)
            token.blacklist()
            return Response({"message": "Log out successfully"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
            return Response({"message": "Image deleted"})
        else:
            raise PermissionDenied("You are not the owner of this image")

    @action(detail=True, methods=['post'])
    def share_with_friend(self, request, pk=None):
        image = self.get_object()
        user_to_share = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_to_share)
            image.share_with_friend.add(user)
            image.save()
            return Response({"message": "Image shared with friend"})
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)