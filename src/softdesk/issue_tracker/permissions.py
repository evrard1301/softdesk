from rest_framework import permissions
from django.shortcuts import get_object_or_404
from . import models


class IsProjectAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(models.Project, pk=view.kwargs.get('id'))
        return request.user == project.author


class IsProjectContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(models.Project, pk=view.kwargs.get('id'))

        if project.author == request.user:
            return True

        contrib = models.Contributor.objects.filter(project=project,
                                                    user=request.user)
        return contrib.count() == 1
