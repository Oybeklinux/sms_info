from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    # path('', include(router.urls)),
    path('signup/teacher/', TeacherSignUpView.as_view()),
    path('signup/payer/', PayerSignUpView.as_view()),
    path('signup/student/', StudentSignUpView.as_view()),
    path('login/', LoginView.as_view(), name='auth-token'),
    path('logout/', LogoutView.as_view())
]
