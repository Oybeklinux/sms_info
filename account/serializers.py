from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    # phone = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name','surname','last_name','role', 'username', 'email', 'telegram',  'phone', 'dob', 'gender']

    # def validate_first_name(self, value):
    #     if not value:
    #         raise serializers.ValidationError("first_name field required.")
    #     return value
    #
    # def validate_surname(self, value):
    #     if not value:
    #         raise serializers.ValidationError("surname field required.")
    #     return value
    #
    # def validate_phone(self, value):
    #
    #     if not value:
    #         raise serializers.ValidationError("phone field required.")
    #     return value
    #


class UserSignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role', 'dob',
                  'first_name', 'last_name', 'surname', 'gender', 'phone', 'telegram']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):

        user = User(
            username=self.validated_data['username'],
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

        if 'role' in self.validated_data:
            user.role=self.validated_data['role']
        if 'email' in self.validated_data:
            user.email=self.validated_data['email']
        if 'first_name' in self.validated_data:
            user.first_name=self.validated_data['first_name']
        if 'last_name' in self.validated_data:
            user.last_name=self.validated_data['last_name']
        if 'telegram' in self.validated_data:
            user.telegram=self.validated_data['telegram']
        if 'dob' in self.validated_data:
            user.dob=self.validated_data['dob']
        if 'gender' in self.validated_data:
            user.gender=self.validated_data['gender']
        if 'phone' in self.validated_data:
            user.phone=self.validated_data['phone']
        if 'surname' in self.validated_data:
            user.surname=self.validated_data['surname']

        user.save()
        return user

