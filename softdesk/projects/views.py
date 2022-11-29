from rest_framework import viewsets, mixins
from rest_framework import permissions
from . import serializers
from . import models


class ProjectView(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    
    serializer_class = serializers.ProjectSerializer
    
    def get_queryset(self):
        return models.Project.objects.all()

    def get_permissions(self):
        return [
            permissions.IsAuthenticated()
        ]

