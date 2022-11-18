from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions as rest_permissions
from rest_framework import status
from rest_framework.response import Response
from . import models
from authentication import models as auth_models
from authentication import serializers as auth_serializers
from . import serializers
from . import permissions


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProjectSerializer

    def create(self, request):
        data = request.data
        project = models.Project.create_project(
            request.user,
            title=data.get('title'),
            description=data.get('description'),
            type=data.get('type')
        )
        
        project.save()
        
        return Response({})

    def list(self, request):
        # TODO
        return Response({})

    def get_queryset(self):
        return models.Project.objects.all()

    def get_permissions(self):
        return [rest_permissions.IsAuthenticated()]


class ContributorAPIView(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = serializers.ContributorSerializer

    def get_permissions(self):
        perms = {
            'create': [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectAuthor()
            ],
            'list': [
                rest_permissions.IsAuthenticated(),
                permissions.IsProjectContributor()
            ]
        }
        
        return perms.get(self.action, perms.get('create'))
    
    def create(self, request, *args, **kwargs):
        user = get_object_or_404(auth_models.User,
                                 pk=request.POST.get('user_id'))

        project = get_object_or_404(models.Project, pk=kwargs.get('id'))        

        if models.Contributor.objects.filter(user=user,
                                             project=project).count() > 0:
            return Response(data={'status': 'already a contributor'},
                            status=status.HTTP_409_CONFLICT)
        
        contributor = models.Contributor(user=user, project=project)
        contributor.save()
        
        return Response(serializers.ContributorSerializer(contributor).data)

    def list(self, *args, **kwargs):
        project = get_object_or_404(models.Project, pk=kwargs['id'])
        contributors = models.Contributor.objects.filter(project=project.id)
        users = [contrib.user for contrib in contributors]
        ser = auth_serializers.UserSerializer(users, many=True)
        
        return Response(ser.data)
