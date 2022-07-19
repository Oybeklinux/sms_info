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


class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = '__all__'


class LessonStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonStudent
        fields = '__all__'
