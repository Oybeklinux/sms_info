from rest_framework import serializers
from rest_framework.response import Response

from .models import *
from account.models import User

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):
        monthes = GroupMonth.objects.filter(group=instance).order_by('month').values()
        # monthes = [month[0] for month in monthes]
        total = GroupStudent.objects.filter(group=instance).count()
        print( "group", instance.name, "total:", total)
        return {
            "id": instance.id,
            "created": instance.created,
            "name": instance.name,
            "start_time": instance.start_time,
            "duration_hours": instance.duration_hours,
            "duration_monthes": instance.duration_monthes,
            "even": instance.even,
            "specialty_id": instance.specialty.id if instance.specialty else None,
            "specialty_name": instance.specialty.name if instance.specialty else None,
            "teacher_id": instance.teacher.id if instance.specialty else None,
            "teacher_name": f"{instance.teacher.surname} {instance.teacher.first_name}"  if instance.specialty else None,
            "groupmonth": monthes,
            "students_num": total
        }


class GroupMonthSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMonth
        fields = '__all__'

    def to_representation(self, instance):
        lessons = Lesson.objects.filter(groupmonth=instance).order_by('date').values()

        return {
            "id": instance.id,
            "month": instance.month,
            "name": instance.name,
            "group": instance.group.id,
            "lessons": lessons
        }


# class GroupStudentSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = GroupStudent
#         fields = '__all__'
#
#     def to_representation(self, instance): #group
#         students = GroupStudent.objects.filter(group=instance).order_by('user__surname').values()
#
#         return {
#             "id": instance.id,
#             "month": instance.month,
#             "name": instance.name,
#             "group": instance.group.id,
#             "students": students
#         }



class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = '__all__'


class LessonStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonStudent
        fields = '__all__'

    def to_representation(self, instance):
        lessonstudent = instance
        user = User.objects.get(id=instance.student.id)
        return {
            "id": lessonstudent.id,
            "homework_done": lessonstudent.homework_done,
            "is_available": lessonstudent.is_available,
            "sms_sent": lessonstudent.sms_sent,
            "lesson": lessonstudent.lesson.id,
            "student": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "surname": user.surname,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "gender": user.gender,
            "phone": user.phone,
            "telegram": user.telegram,
            "dob": user.dob,
            "work": user.work,
            "study": user.study,
            "paid_by_parents": user.paid_by_parents,
        }

    def create(self, validated_data):
        obj, created = LessonStudent.objects.update_or_create(
            student=validated_data.get('student', None),
            lesson=validated_data.get('lesson', None),
            defaults={
                'homework_done': validated_data.get('homework_done', None),
                'is_available': validated_data.get('is_available', None)
            },
        )

        return obj


class GroupStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupStudent
        fields = '__all__'

    def to_representation(self, instance):
        user = User.objects.get(id=instance.student.id)
        return {
            "id": instance.id,
            "created": instance.created,
            "group": instance.group.id,
            "student": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "surname": user.surname,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "gender": user.gender,
            "phone": user.phone,
            "telegram": user.telegram,
            "dob": user.dob,
            "work": user.work,
            "study": user.study,
            "paid_by_parents": user.paid_by_parents,
        }


class GroupStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupStudent
        fields = '__all__'

    def to_representation(self, instance):
        user = User.objects.get(id=instance.student.id)
        return {
            "id": instance.id,
            "created": instance.created,
            "group": instance.group.id,
            "student": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "surname": user.surname,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "gender": user.gender,
            "phone": user.phone,
            "telegram": user.telegram,
            "dob": user.dob,
            "work": user.work,
            "study": user.study,
            "paid_by_parents": user.paid_by_parents,
        }


class GroupStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupStudent
        fields = '__all__'

    def to_representation(self, instance):
        user = User.objects.get(id=instance.student.id)
        return {
            "id": instance.id,
            "created": instance.created,
            "group": instance.group.id if hasattr(instance, 'group') else None,
            "student": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "surname": user.surname,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "gender": user.gender,
            "phone": user.phone,
            "telegram": user.telegram,
            "dob": user.dob,
            "work": user.work,
            "study": user.study,
            "paid_by_parents": user.paid_by_parents,
        }
