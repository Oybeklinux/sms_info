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
        fields = ['username', 'email', 'password', 'password2', 'role', 'dob',
                  'first_name', 'last_name', 'gender', 'phone', 'telegram']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            telegram=self.validated_data['telegram'],
            dob=self.validated_data['dob'],
            gender=self.validated_data['gender'],
            phone=self.validated_data['phone']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "Password is not match"})
        user.set_password(password)

        if user.role == "admin":
            user.is_staff = True
        elif user.role == "superadmin":
            user.is_superuser = True
            user.is_staff = True

        user.save()
        return user

