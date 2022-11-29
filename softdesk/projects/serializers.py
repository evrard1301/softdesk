from rest_framework.serializers import ModelSerializer
from . import models


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = models.Project
        fields = [
            'id',
            'title',
            'description',
            'type'
        ]
