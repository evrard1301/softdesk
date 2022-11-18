from rest_framework import permissions
from django.shortcuts import get_object_or_404
from . import models


class IsProjectAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(models.Project, pk=view.kwargs.get('id'))

        contrib = models.Contributor.objects.filter(project=project,
                                                    user=request.user)
        return contrib.count() == 1 and contrib[0].role == models.Contributor.ROLE_OWNER


class IsProjectContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(models.Project, pk=view.kwargs.get('id'))

        contrib = models.Contributor.objects.filter(project=project,
                                                    user=request.user)
        return contrib.count() == 1
