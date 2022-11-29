from rest_framework import viewsets, mixins
from rest_framework import permissions as rest_permissions
from . import serializers
from . import models
from . import permissions


class ProjectView(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    
    serializer_class = serializers.ProjectSerializer
    
    def get_queryset(self):
        return models.Project.objects.all()

    def get_permissions(self):
        if self.action == 'update':
            return [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectAuthor()
            ]
        
        return [
            rest_permissions.IsAuthenticated()
        ]

