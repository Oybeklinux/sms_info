from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken


@api_view(['GET'])
def profile(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        token = token.lstrip("Token ")
        user = User.objects.get(auth_token=token)
    except Exception as error:
        print(error)
        return Response({
            "error": "No such user"
        })
    serializer = UserSerializer(user)
    return Response(serializer.data)


class UserSignUpView(generics.GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer.is_valid(raise_exception=True)

        return Response({
            "user_id": user.id,
            "token": Token.objects.get(user=user).key,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "surname": user.surname,
            "gender": user.gender,
            "phone": user.phone,
            "telegram": user.telegram,
            "dob": user.dob
        })


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)


        return Response({
            'token': token.key,
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
            "dob": user.dob
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['get', 'put', 'patch', 'delete']

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data
        if 'parent' in data:
            user.parent.clear()
            for parent in User.objects.filter(role='payer', id__in=data['parent']):
                user.parent.add(parent)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="teacher")
    serializer_class = PeopleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="student")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get','post']

    def create(self, request, *args, **kwargs):
        data = request.data
        payers = data.pop('payer')
        print(data)
        # Alohida parentni kiritish
        # Alohida student parentni kiritish

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # bulk save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="payer")
    serializer_class = PeopleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']
