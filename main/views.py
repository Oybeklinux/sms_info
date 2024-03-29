from django.db.models.query import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
import re
from .helpers import send_otp_to_phone
from .serializers import *
from django.db.models import Q

from account.models import User
from account.serializers import UserSerializer
import logging

logging.basicConfig(filename="log.txt", level=logging.DEBUG)
logger = logging.getLogger(__name__)


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


def students2gstudents(users):
    groupstudents = []

    for user in users:
        groupstudents.append(GroupStudent(id=user['id'], student_id=user['student'], group_id=user['group']))
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
        lesson = Lesson.objects.get(id=pk)
        lesson.ended = True
        lesson.save()
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
    filterset_fields = ['groupmonth', 'id']

    def create(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data['date'], list):
            serializer = LessonSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        else:
            groupmonth = data['groupmonth']
            dates = [date.fromisoformat(dt) for dt in data['date']]
            for dt in data['date']:
                data = {"groupmonth": groupmonth, "date": dt}
                serializer = LessonSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()  # bulk save

            Lesson.objects.exclude(date__in=dates).delete()
            lessons = Lesson.objects.filter(groupmonth=groupmonth)
            serializer = LessonSerializer(lessons, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# class LessonStudentViewSet(viewsets.ModelViewSet):
#     queryset = LessonStudent.objects.all()
#     serializer_class = LessonStudentSerializer
#     # http_method_names = ['get', 'post']


class GroupStudentViewSet(viewsets.ModelViewSet):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def list(self, request):
        group = request.query_params.get('students_to_add', None)
        if not group:
            serializer = GroupStudentSerializer(self.queryset, many=True)
            return Response(serializer.data)
        else:
            try:
                if Group.objects.get(id=int(group)):
                    pass
            except Exception as error:
                print(error)
                return Response({"message": "No such group"}, status=status.HTTP_404_NOT_FOUND)

            users = GroupStudent.objects.filter(group=group).values('id', 'student', 'group')
            users_id = [user['student'] for user in users]

            users1 = User.objects.exclude(id__in=users_id)
            users1 = users1.filter(role='student')
            users1 = [{'id': None, 'student': user.id, "group": None} for user in users1]

            users = list(users) + users1

            groupstudents = students2gstudents(users)

            serializer = GroupStudentSerializer(groupstudents, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data['student'], list):
            serializer = GroupStudentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()  # bulk save
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        else:
            group = data['group']
            students = [st for st in data['student']]
            for st in students:
                data = {"group": group, "student": st}
                serializer = GroupStudentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

            GroupStudent.objects.exclude(student__in=students).delete()
            groupstudents = GroupStudent.objects.filter(group=group)
            serializer = GroupStudentSerializer(groupstudents, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def send_sms(request, lesson_id):
    lessonstudents = LessonStudent.objects.filter(lesson=lesson_id)
    if lessonstudents:
        errors = []
        for lessonstudent in lessonstudents:
            payer_name = ""
            if not lessonstudent.sms_sent:
                student = lessonstudent.student

                if not student.paid_by_parents:
                    if lessonstudent.student.phone:
                        phone = lessonstudent.student.phone
                        payer_name = f"{student.surname} {student.first_name}"
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
                    logger.info('+++ 2 +++')
                    payer = lessonstudent.student.payer
                    phone = payer.phone
                    payer_name = f"{payer.surname} {payer.first_name}"
                logger.info('+++ 3 +++')
                student_name = f"{student.surname} {student.first_name}"
                study_date = lessonstudent.lesson.date.strftime("%d-%m-%Y")
                phone = re.sub(r'[^\d]', '', phone)
                logger.info('+++ 4 +++')
                data = {
                    "phone_number": phone,
                    "payer_name": payer_name,
                    "student_name": student_name,
                    "study_date": study_date,
                    "is_available": lessonstudent.is_available,
                    "homework_done": lessonstudent.homework_done
                }
                ok, error = send_otp_to_phone(**data)
                logger.info('+++ 5 +++')
                if ok:
                    lessonstudent.sms_sent = True
                    lessonstudent.save()
                else:
                    errors.append({
                        "student_id": student.id,
                        "message": error
                    })
                    continue
                logger.info('+++ 6 +++')
        serializer = LessonStudentSerializer(lessonstudents, many=True)
        return Response({"students": serializer.data, "errors": errors}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
