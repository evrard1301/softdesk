from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Project


class IsProjectAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, pk=view.kwargs.get('id'))
        return request.user == project.author
