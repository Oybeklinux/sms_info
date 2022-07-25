from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GroupMonthViewSet(viewsets.ModelViewSet):
    queryset = GroupMonth.objects.all()
    serializer_class = GroupMonthSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['POST'])
def add_lessons(request, pk):
    objects = []
    for dt in request.data:
        objects.append(dict(groupmonth=pk, date=dt))

    serializer = LessonSerializer(data=objects, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['groupmonth']


class LessonStudentViewSet(viewsets.ModelViewSet):
    queryset = LessonStudent.objects.all()
    serializer_class = LessonStudentSerializer


class GroupStudentViewSet(viewsets.ModelViewSet):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer
