from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to modify the object.
    """

    def has_permission(self, request, view):
        # Allow read-only access to anyone (safe methods: GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write access only to admins
        return request.user and request.user.is_staff
