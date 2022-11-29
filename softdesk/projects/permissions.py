from rest_framework.permissions import BasePermission
from . import models


class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        project = view.get_object()
        role = models.Contributor.AUTHOR_ROLE
        return models.Contributor.objects.filter(user=user,
                                                 project=project,
                                                 role=role).count() > 0
