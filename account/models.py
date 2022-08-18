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
        ("admin", "Admin"),
        ("superAdmin", "SuperAdmin"),
    ]
    role = models.CharField(max_length=50, choices=ROLE, default="student")
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, default="man", choices=GENDER)
    phone = models.CharField(max_length=50)
    telegram = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50)
    study = models.BooleanField(default=None, null=True)
    work = models.BooleanField(default=None, null=True)
    paid_by_parents = models.BooleanField(default=False)
    # payer = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    parent = models.ManyToManyField("User", null=True, related_name="parents")

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
