from rest_framework import permissions
from .models import User

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)


class CustomPermission(permissions.BasePermission):
    role_name = ''
    def has_permission(self, request, view):
        if request.user:
            if request.user.is_authenticated:
                if request.user.is_admin:
                    return True
                else:
                    print(getattr(request.user, self.role_name))
                    if getattr(request.user, self.role_name):
                        return True
                    return False
            else:
                return False
        else:
            return False

class IsVerified(CustomPermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.verified)

def check_custom_permissions(user, allowed_roles):
    if user:
        if user.is_authenticated:
            if user.is_admin:
                return True
            else:
                pers = [getattr(user, x) for x in allowed_roles]
                if any(pers) == True:
                    return True
                return False
        else:
            return False
    else:
        return False