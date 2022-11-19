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
            ],
            'list': [
                rest_permissions.IsAuthenticated()
            ],
            'retrieve': [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectContributor()
            ],
            'update': [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectOwner()
            ],
            'destroy': [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectOwner()
            ]
        }

        if self.action not in perms.keys():
            raise Exception(f'unknown action "{self.action}"')
        
        return perms.get(self.action)
        
    def create(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        type = request.POST.get('type')

        project = models.Project(
            title=title,
            description=description,
            type=type
        )

        try:
            project.full_clean()
        
            project.save()

            models.Contributor.objects.create(
                project=project,
                user=request.user,
                role=models.Contributor.ROLE_OWNER
            )

            ser = serializers.ProjectSerializer(project)
            
            return Response(data=ser.data,
                            status=status.HTTP_200_OK)
        except ValidationError:
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        projects = [
            c.project
            for c
            in models.Contributor.objects.filter(user=request.user)
        ]
        data = serializers.ProjectSerializer(projects, many=True).data
        return Response(data)

    def retrieve(self, request, pk):
        obj = models.Project.objects.filter(id=pk).first()
        self.check_object_permissions(request, obj)
        data = serializers.ProjectSerializer(obj).data
        
        return Response(data)

    def update(self, request, pk):
        project = get_object_or_404(models.Project, pk=pk)
        self.check_object_permissions(request, project)
        
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.type = request.POST.get('type')        
        project.save()
        
        return Response(serializers.ProjectSerializer(project).data)
    
    def destroy(self, request, pk):
        project = get_object_or_404(models.Project, pk=pk)
        self.check_object_permissions(request, project)
        project.delete()
        return Response({})


class ContributorViewSet(viewsets.ViewSet):
    def get_permissions(self):
        perms = {
            'create': [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectOwner()
            ],
            'destroy': [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectOwner()
            ],
            'list': [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectContributor()
            ]

        }
        
        if self.action not in perms.keys():
            raise Exception(f'unknown action "{self.action}"')
        
        return perms.get(self.action)

    def create(self, request, project_pk):
        project = get_object_or_404(models.Project, pk=project_pk)
        
        user = get_object_or_404(
            auth_models.User,
            pk=request.POST.get('user_id')
        )

        self.check_object_permissions(request, project)

        models.Contributor.objects.create(
            user=user,
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )
        
        return Response()

    def list(self, request, project_pk):
        project = get_object_or_404(models.Project, pk=project_pk)
        self.check_object_permissions(request, project)
        
        users = [
            contributor.user for contributor
            in models.Contributor.objects.filter(project=project).all()
        ]

        data = auth_serializers.UserSerializer(users, many=True).data

        return Response(data)

    def destroy(self, request, project_pk, pk):
        project = get_object_or_404(models.Project, pk=project_pk)
        user = get_object_or_404(auth_models.User, pk=pk)
        self.check_object_permissions(request, project)
        
        res = models.Contributor.objects.filter(project=project,
                                                user=user)
        
        data = auth_serializers.UserSerializer(user).data
        
        if len(res) == 1:
            user.delete()
        
        return Response(data)
        
