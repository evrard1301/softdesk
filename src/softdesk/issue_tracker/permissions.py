from rest_framework import permissions
from . import models


class IsProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        contrib = models.Contributor.objects.filter(
            project=obj,
            user=request.user
        )
        
        return contrib.count() == 1 \
            and contrib[0].role == models.Contributor.ROLE_OWNER


class IsProjectContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        contrib = models.Contributor.objects.filter(project=obj,
                                                    user=request.user)
        return contrib.count() == 1
