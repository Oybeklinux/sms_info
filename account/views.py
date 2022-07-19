from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken


class TeacherSignUpView(generics.GenericAPIView):
    serializer_class = TeacherSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "User created"
            # "user_id": user.pk
        })


class StudentSignUpView(generics.GenericAPIView):
    serializer_class = StudentSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "User created"
        })


class PayerSignUpView(generics.GenericAPIView):
    serializer_class = PayerSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "User created"
        })


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(dir(user))
        print(user.id)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_teacher': user.is_teacher,
            'is_student': user.is_student,
            'is_payer': user.is_payer
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)