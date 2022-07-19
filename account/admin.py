from django.contrib import admin

# Register your models here.
from .models import Teacher, Student, Payer, User

admin.site.register(Teacher)
admin.site.register(Payer)
admin.site.register(Student)
admin.site.register(User)