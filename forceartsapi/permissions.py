"""Custom permission module"""
from rest_framework import permissions


class CreateAndUpdate(permissions.BasePermission):
    """Allow authenticated users to create and update wallpaper"""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.method == 'PATCH'
