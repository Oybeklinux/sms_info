import uuid

from django.db import models

# Create your models here.
from account.models import User


class Specialty(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    duration_hours = models.FloatField(default=1.5)
    duration_monthes = models.IntegerField(default=6)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Lesson(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    theme = models.CharField(max_length=300)
    comment = models.CharField(max_length=300, null=True)
    date = models.DateField()


class LessonStudent(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    homework_done = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)