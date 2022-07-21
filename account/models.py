import uuid

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
# from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    GENDER = [
        ("man", "Man"),
        ("woman", "Woman")
    ]
    ROLE = [
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("payer", "Payer"),
        ("sdmin", "Admin"),
        ("superAdmin", "SuperAdmin"),
    ]
    role = models.CharField(max_length=50, choices=ROLE, default="STUDENT")
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, default="man", choices=GENDER)
    phone = models.CharField(max_length=50,null=True, blank=True)
    telegram = models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
