from django.contrib import admin
from .models import *
admin.site.register(Group)
admin.site.register(Specialty)
admin.site.register(Lesson)
admin.site.register(LessonStudent)
admin.site.register(GroupStudent)
admin.site.register(GroupMonth)

# Register your models here.
