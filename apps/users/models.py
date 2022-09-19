from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class UserRoleChoices(models.TextChoices):
    ADMINISTRATOR = ('ad', _('admin'))
    RESTAURANT_ADMINISTRATOR = ('ra', _('restaurant_admin'))
    EMPLOYEE = ('em', _('employee'))


class CustomUserModel(AbstractBaseUser):
    class Meta:
        db_table = 'users'

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=60)
    role = models.CharField(max_length=2, choices=UserRoleChoices.choices, default=UserRoleChoices.EMPLOYEE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_superuser = None
    groups = None
    user_permissions = None
    last_login = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
