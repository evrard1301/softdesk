from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions as rest_permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import models
from authentication import models as auth_models
from authentication import serializers as auth_serializers
from . import serializers
from . import permissions


class ProjectViewSet(viewsets.ViewSet):

    def get_permissions(self):
        perms = {
            'create': [
                rest_permissions.IsAuthenticated()
            ]
        }

        return perms.get(self.action)
        
    def create(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        type = request.POST.get('type')

        project = models.Project(title=title,
                                 description=description,
                                 type=type)

        try:
            project.full_clean()
        
            project.save()

            models.Contributor.objects.create(project=project,
                                              user=request.user,
                                              role=models.Contributor.ROLE_OWNER)

            ser = serializers.ProjectSerializer(project)
            
            return Response(data=ser.data,
                            status=status.HTTP_200_OK)
        except ValidationError:
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)

        
