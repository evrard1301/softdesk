from django.shortcuts import get_object_or_404
from rest_framework import permissions
from . import models


class IsProjectOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        project_pk = view.kwargs['projects_pk']
        
        contrib = models.Contributor.objects.filter(
            project=get_object_or_404(models.Project, pk=project_pk),
            user=request.user
        )
        
        return contrib.count() == 1 \
            and contrib[0].role == models.Contributor.ROLE_OWNER


class IsProjectContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        project_pk = view.kwargs['projects_pk']
        
        contrib = models.Contributor.objects.filter(
            project=get_object_or_404(models.Project, pk=project_pk),
            user=request.user
        )
        
        return contrib.count() == 1;


class IsProjectOwnerObj(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        contrib = models.Contributor.objects.filter(
            project=obj,
            user=request.user
        )
        
        return contrib.count() == 1 \
            and contrib[0].role == models.Contributor.ROLE_OWNER


class IsProjectContributorObj(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        contrib = models.Contributor.objects.filter(project=obj,
                                                    user=request.user)
        return contrib.count() == 1
