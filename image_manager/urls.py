from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginAPIView, ImageViewSet, LogoutAPIView, RegisterAPIView

router = DefaultRouter()
router.register('image', ImageViewSet)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('share/', ImageViewSet.as_view({'post': 'share_with_friend'}), name='share'),
    path('', include(router.urls)),
]