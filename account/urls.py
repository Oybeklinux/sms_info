from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("teachers", TeacherProfileViewSet)
router.register("students", StudentProfileViewSet)
router.register("payers", PayerProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]
