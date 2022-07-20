from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register("group", GroupViewSet)
router.register("lesson", LessonViewSet)
router.register("specialty", SpecialtyViewSet)
router.register("lesson_student", LessonStudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]