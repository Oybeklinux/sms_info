from rest_framework import serializers
from .models import StudentProfile, User, TeacherProfile, PayerProfile


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class StudentProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentProfile
        fields = '__all__'
    read_only_fields = ('user',)

class TeacherProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherProfile
        fields = '__all__'

    read_only_fields = ('user',)

class PayerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = PayerProfile
        fields = '__all__'

    read_only_fields = ('user',)