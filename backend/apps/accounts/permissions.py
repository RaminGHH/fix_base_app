from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import BasePermission, SAFE_METHODS

class CsrfRequired(BasePermission):
    """Explicitly protects cookie auth AND anonymous login against CSRF"""
    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            SessionAuthentication().enforce_csrf(request)
        return True