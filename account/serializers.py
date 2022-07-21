from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'id']


class UserSignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "Password is not match"})
        user.set_password(password)
        if 'role' not in self.validated_data or not self.validated_data['role']:
            user.role = 'STUDENT'
        else:
            user.role = self.validated_data['role']
        user.save()
        if user.role == "TEACHER":
            Teacher.objects.create(user=user)
        elif user.role == "STUDENT":
            Student.objects.create(user=user)
        elif user.role == "PAYER":
            Payer.objects.create(user=user)
        elif user.role == "ADMIN":
            user.is_staff = True
            user.save()
        elif user.role == "SUPERADMIN":
            user.is_superuser = True
            user.is_staff = True
            user.save()
        return user

#     delete update get ni yozib chiqish kerak


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = '__all__'


class PayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payer
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


