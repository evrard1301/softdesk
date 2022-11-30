from rest_framework import viewsets, mixins
from rest_framework import permissions as rest_permissions
from . import serializers
from . import models
from . import permissions


class ProjectView(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    
    serializer_class = serializers.ProjectSerializer
    
    def get_queryset(self):
        if self.action == 'list':
            user = self.request.user
            contribs = models.Contributor.objects.filter(user=user)
            return [contrib.project for contrib in contribs]
                    
        return models.Project.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectAuthor()
            ]
        elif self.action in ['retrieve']:
            return [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectRelated()
            ]
        
        return [
            rest_permissions.IsAuthenticated()
        ]

