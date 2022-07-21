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
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    ROLE = [
        ("TEACHER", "Teacher"),
        ("STUDENT", "Student"),
        ("PAYER", "Payer"),
        ("ADMIN", "Admin"),
        ("SUPERADMIN", "SuperAdmin"),
    ]
    role = models.CharField(max_length=50, choices=ROLE, default="STUDENT")
    # is_teacher = models.BooleanField(default=False)
    # is_payer = models.BooleanField(default=False)
    # is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# class StudentManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(is_student=True)


# class TeacherManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(is_teacher=True)
#
#
# class PayerManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(is_payer=True)
#
#
class Payer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="payers")
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    surname = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    who = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="students")
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    surname = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="students", default="empty.png")
    email = models.EmailField(blank=True, null=True)
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE, null=True)
    study = models.CharField(max_length=100, blank=True, null=True)
    work = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teachers")
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    surname = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# @receiver(post_save, sender=Payer)
# def create_payer_profile(sender, instance, created, **kwargs):
#     if created and instance.role == User.Role.PAYER:
#         Payer.objects.create(user=instance)
#
#
#
#
# @receiver(post_save, sender=Student)
# def create_student_profile(sender, instance, created, **kwargs):
#     if created and instance.role == User.Role.STUDENT:
#         StudentProfile.objects.create(user=instance)
#
#
#
#
# @receiver(post_save, sender=Teacher)
# def create_teacher_profile(sender, instance, created, **kwargs):
#     if created and instance.role == User.Role.TEACHER:
#         TeacherProfile.objects.create(user=instance)
#
#
