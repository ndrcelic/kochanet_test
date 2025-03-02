from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='image_manager_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='image_manager_user_permissions', blank=True)
    phone_number = models.CharField(max_length=11, unique=False, blank=True)
    city = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=120, blank=True)
    birthday = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='shared', blank=True)
