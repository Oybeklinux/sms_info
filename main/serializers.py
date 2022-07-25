from rest_framework import serializers
from .models import *


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
            "groupmonth": monthes
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

class GroupStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupStudent
        fields = '__all__'
