from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
# router.register("teacher", TeacherViewSet)
# router.register("student", StudentViewSet)
# router.register("payer", PayerViewSet)
router.register("user", UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('signup/', UserSignUpView.as_view()),
    path('login/', LoginView.as_view(), name='auth-token'),
    path('logout/', LogoutView.as_view()),
]
