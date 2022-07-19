from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_student)


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_teacher)


class IsPayer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.payer)