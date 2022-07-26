import uuid
from datetime import date

from django.db import models

# Create your models here.
from account.models import User


class Specialty(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)


class Group(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)
    start_time = models.TimeField()
    duration_hours = models.FloatField(default=1.5)
    duration_monthes = models.IntegerField(default=6)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    even = models.BooleanField(default=True) # juft kunlarimi

    def __str__(self):
        return f"{self.name}"


class GroupMonth(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_monthes")
    month = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.month)


class Lesson(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    groupmonth = models.ForeignKey(GroupMonth, on_delete=models.CASCADE, null=True, related_name="groupmonth_lessons")
    theme = models.CharField(max_length=300, null=True, blank=True)
    comment = models.CharField(max_length=300, null=True)
    date = models.DateField()

    class Meta:
        unique_together = ('date', 'groupmonth')

    def __str__(self):
        return f"{self.date}"


class LessonStudent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    homework_done = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} {self.lesson}"


class GroupStudent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_monthes")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_students")
    created = models.DateField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('created', 'student', 'group')

    def __str__(self):
        return f"{self.student} {self.group}"
