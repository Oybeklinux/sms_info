from django.db.models.query import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
import re
from .helpers import send_otp_to_phone
from .serializers import *
from django.db.models import Q

from account.models import User

from account.serializers import UserSerializer


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
    if 'date' not in request.data:
        raise ValueError('date required')

    for dt in request.data['date']:
        objects.append(dict(groupmonth=pk, date=dt))

    serializer = LessonSerializer(data=objects, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST', 'GET'])
def add_student_to_group(request, group_id):
    if request.method == 'POST':
        if Group.objects.filter(id=group_id).count() == 0:
            return Response({"message": "No such group"}, status=status.HTTP_404_NOT_FOUND)

        objects = []
        if 'students' not in request.data:
            raise ValueError('students required')

        for student in request.data['students']:
            objects.append(dict(student=student, group=group_id))

        serializer = GroupStudentSerializer(data=objects, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        try:
            if Group.objects.get(id=group_id):
                pass
        except Exception as error:
            print(error)
            return Response({"message": "No such group"}, status=status.HTTP_404_NOT_FOUND)

        users = GroupStudent.objects.filter(Q(group=group_id)).values('student', 'group')
        users_id = [user['student'] for user in users]

        users1 = User.objects.exclude(id__in=users_id)
        users1 = users1.filter(role='student')
        users1 = [{'student': user.id, "group": None} for user in users1]

        users = list(users) + users1

        groupstudents = students2gstudents(users)

        serializer = GroupStudentSerializer(groupstudents, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def students2gstudents(users):
    groupstudents = []

    for user in users:
        groupstudents.append(GroupStudent(student_id=user['student'], group_id=user['group']))
    return groupstudents


def gstudents2lstudents(groupstudents, lesson):
    lessonstudents = []

    for groupstudent in groupstudents:
        lessonstudent = LessonStudent(
            homework_done=False,
            is_available=False,
            lesson=lesson,
            sms_sent=False,
            student=groupstudent.student
        )
        lessonstudents.append(lessonstudent)
    return lessonstudents


@api_view(['POST', 'GET'])
def add_hw_and_is_available(request, pk):
    if request.method == 'POST':
        objects = []
        if 'students' not in request.data:
            raise ValueError('students required')

        for obj in request.data['students']:
            hw = obj["homework_done"] if 'homework_done' in obj else False
            is_av = obj["is_available"] if 'is_available' in obj else False
            student = obj["student"]

            object = dict(
                homework_done=hw,
                is_available=is_av,
                student=student,
                lesson=pk
            )

            objects.append(object)

        serializer = LessonStudentSerializer(data=objects, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(objects, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        try:
            lessonstudents = LessonStudent.objects.filter(lesson=pk)

            if lessonstudents:
                serializer = LessonStudentSerializer(lessonstudents, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                lesson = Lesson.objects.get(pk=pk)
                group = lesson.groupmonth.group
                groupstudents = GroupStudent.objects.filter(group=group)
                lessonstudents = gstudents2lstudents(groupstudents, lesson)
                serializer = LessonStudentSerializer(lessonstudents, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as error:
            print(error)
            return Response(status=status.HTTP_204_NO_CONTENT)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('date')
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['groupmonth']


# class LessonStudentViewSet(viewsets.ModelViewSet):
#     queryset = LessonStudent.objects.all()
#     serializer_class = LessonStudentSerializer
#     # http_method_names = ['get', 'post']


class GroupStudentViewSet(viewsets.ModelViewSet):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']


@api_view(['POST'])
def send_sms(request, lesson_id):
    lessonstudents = LessonStudent.objects.filter(lesson=lesson_id)
    if lessonstudents:
        errors = []
        for lessonstudent in lessonstudents:

            if not lessonstudent.sms_sent:
                student = lessonstudent.student

                if not student.paid_by_parents:
                    if lessonstudent.student.phone:
                        phone = lessonstudent.student.phone
                    else:
                        errors.append({
                            "student_id": student.id,
                            "message": "No student phone provided"
                        })
                        continue
                else:
                    if not lessonstudent.student.payer:
                        errors.append({
                            "student_id": student.id,
                            "message": "No payer is provided"
                        })
                        continue
                    if not lessonstudent.student.payer.phone:
                        errors.append({
                            "student_id": student.id,
                            "message": "No phone of payer is provided"
                        })
                        continue

                    phone = lessonstudent.student.payer.phone

                message = f'Название урока: {lessonstudent.lesson.theme if lessonstudent.lesson.theme else ""}\n' \
                          f'Число: {lessonstudent.lesson.date}\n' \
                          f'Домашняя работа: {"сделана" if lessonstudent.homework_done else "не сделана"}\n' \
                          f'Присутствие на уроке: {"был(а)" if lessonstudent.is_available else "не был(а)"}'
                phone = re.sub(r'[^\d]', '', phone)
                ok, error = send_otp_to_phone(phone, message)

                if ok:
                    lessonstudent.sms_sent = True
                    lessonstudent.save()
                else:
                    errors.append({
                        "student_id": student.id,
                        "message": error
                    })
                    continue
        serializer = LessonStudentSerializer(lessonstudents, many=True)
        return Response({"students": serializer.data, "errors": errors}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
