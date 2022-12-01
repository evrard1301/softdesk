from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework import permissions as rest_permissions
from . import serializers
from . import models
from . import permissions
from authentication.models import User


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
            contribs = models.Collaborator.objects.filter(user=user)
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

    def perform_create(self, serializer):
        project = serializer.save()
        models.Collaborator.objects.create(user=self.request.user,
                                          project=project,
                                          role=models.Collaborator.AUTHOR_ROLE)


class UserView(mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):
    serializer_class = serializers.CollaboratorSerializer

    def get_permissions(self):
        if self.action in ['list']:
            return [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectRelated()
            ]

        return [
            rest_permissions.IsAuthenticated(),
            permissions.IsProjectAuthor()
        ]

    def get_queryset(self):
        return models.Collaborator.objects.all()

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        project = get_object_or_404(models.Project, pk=kwargs['project_pk'])
        user = request.user
        role = request.POST.get('role')

        contrib = models.Collaborator(project=project,
                                     user=user,
                                     role=role)
        try:
            contrib.full_clean()
            contrib.save()
        except Exception:
            Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        project = get_object_or_404(
            models.Project,
            pk=kwargs.get('project_pk')
        )

        user = get_object_or_404(User, pk=pk)

        contrib = models.Collaborator.objects.get(project=project,
                                                  user=user)
        contrib.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueView(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    serializer_class = serializers.IssueSerializer
    queryset = models.Issue.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [
                rest_permissions.IsAuthenticated(),
                permissions.IsIssueAuthor()
            ]

        return [
            rest_permissions.IsAuthenticated(),
            permissions.IsProjectRelated()
        ]

    def perform_create(self, serializer):
        serializer.save(project=get_object_or_404(
            models.Project,
            pk=self.kwargs.get('project_pk')
        ))

    
class CommentView(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
    
    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectRelated(),
                permissions.IsCommentAuthor()
            ]

        return [
            rest_permissions.IsAuthenticated(),
            permissions.IsProjectRelated()
        ]        
    
    def perform_create(self, serializer):
        serializer.save(issue=get_object_or_404(
            models.Issue,
            pk=self.kwargs['issue_pk']
        ))
