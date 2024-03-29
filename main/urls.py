from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register("group", GroupViewSet)
router.register("groupmonth", GroupMonthViewSet)
router.register("lesson", LessonViewSet)
router.register("specialty", SpecialtyViewSet)
router.register("group_student", GroupStudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lesson_student/<int:pk>/', add_hw_and_is_available),
    path('send_sms/<int:lesson_id>/', send_sms),
]
