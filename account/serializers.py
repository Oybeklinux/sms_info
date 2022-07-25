from rest_framework import serializers
from .models import *
from main.models import GroupStudent, Group
from main.serializers import GroupSerializer

class UserSerializer(serializers.ModelSerializer):
    # phone = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name','surname','last_name','role', 'username', 'email', 'telegram',  'phone', 'dob', 'gender', 'study', 'work', 'paid_by_parents']

    def to_representation(self, instance):
        token = Token.objects.filter(user=instance).values('key')[0]
        token = token['key']
        user = instance
        group_id_list = GroupStudent.objects.filter(student=user).values_list('group_id')
        group_id_list = [obj[0] for obj in group_id_list]
        groups = Group.objects.filter(pk__in=group_id_list)
        groups = GroupSerializer(groups, many=True)
        # print("group", group_id_list)
        # grps = []
        # for gr in groups.data:
        #     del gr['groupmonth']
        #     grps.append(gr)

        return {
            'token': token,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "user_id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "surname": user.surname,
            "gender": user.gender,
            "phone": user.phone,
            "telegram": user.telegram,
            "dob": user.dob,
            "work": user.work,
            "study": user.study,
            "paid_by_parents": user.paid_by_parents,
            "groups": groups
        }

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
                  'first_name', 'last_name', 'surname', 'gender', 'phone', 'telegram', 'work', 'study', 'paid_by_parents']
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

