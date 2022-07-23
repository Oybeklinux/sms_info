from rest_framework import serializers
from .models import *
from account.serializers import UserSerializer


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):

        return {
            "id": instance.id,
            "created": instance.created,
            "name": instance.name,
            "start_time": instance.start_time,
            "duration_hours": instance.duration_hours,
            "duration_monthes": instance.duration_monthes,
            "specialty_id": instance.specialty.id,
            "specialty_name": instance.specialty.name,
            "teacher_id": instance.teacher.id,
            "teacher_name": f"{instance.teacher.surname} {instance.teacher.first_name}",
        }


class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = '__all__'


class LessonStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonStudent
        fields = '__all__'
