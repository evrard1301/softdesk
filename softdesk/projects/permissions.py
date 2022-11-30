from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from . import models


def get_project(view):
    if 'project_pk' in view.kwargs.keys():
        return get_object_or_404(models.Project, pk=view.kwargs['project_pk'])
    else:
        return view.get_object()

    
class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        project = get_project(view)
        
        role = models.Contributor.AUTHOR_ROLE
        return models.Contributor.objects.filter(user=user,
                                                 project=project,
                                                 role=role).count() > 0


class IsProjectRelated(BasePermission):
    def has_permission(self, request, view):        
        user = request.user
        project = get_project(view)
        return models.Contributor.objects.filter(user=user,
                                                 project=project).count() > 0
