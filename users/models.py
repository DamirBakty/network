from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.generics import get_object_or_404

# Create your models here.

class UserManager(BaseUserManager):
    @staticmethod
    def get_user(data):
        return get_object_or_404(User, **data)

    @staticmethod
    def _validate_user(email: str):
        if not email:
            raise ValueError('Users must have an email address')


    def create_user(self, email: str, password: str = None) -> 'User':

        self._validate_user(email=email)

        user = self.model(
            email=self.normalize_email(email),
            is_active=False,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str = None) -> 'User':
        self._validate_user(email=email)

        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password(password)
        user.save()

        return user


class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
