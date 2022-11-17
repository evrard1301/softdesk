from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from . import models
from . import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProjectSerializer

    def create(self, request):
        data = request.data
        project = models.Project(title=data.get('title'),
                                 description=data.get('description'),
                                 type=data.get('type'))
        project.author = request.user
        project.save()
        return Response({})

    def list(self, request):
        projects = models.Project.objects.filter(author=request.user).all()
        data = serializers.ProjectSerializer(projects, many=True).data
        return Response(data)

    def get_queryset(self):
        return models.Project.objects.all()

    def get_permissions(self):
        return [permissions.IsAuthenticated()]
