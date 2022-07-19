from django.contrib import admin

# Register your models here.
from .models import TeacherProfile, StudentProfile, PayerProfile, User

admin.site.register(TeacherProfile)
admin.site.register(PayerProfile)
admin.site.register(StudentProfile)
admin.site.register(User)