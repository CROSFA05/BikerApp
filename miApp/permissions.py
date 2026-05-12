from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class SameGroupOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if not request.user.grupo_biker or not obj.grupo_biker:
            return obj == request.user
        return request.user.grupo_biker == obj.grupo_biker


class IsLeaderOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'lider'):
            return obj.lider == request.user
        return False


class SameGroupViewOwnerEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'usuario') and obj.usuario:
                if not request.user.grupo_biker or not obj.usuario.grupo_biker:
                    return obj.usuario == request.user
                return request.user.grupo_biker == obj.usuario.grupo_biker
            return True
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        return obj == request.user
