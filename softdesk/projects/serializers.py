from rest_framework.serializers import ModelSerializer
from . import models
from rest_framework import serializers
from rest_framework_nested import serializers as nserializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = models.Project
        fields = [
            'id',
            'title',
            'description',
            'type'
        ]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributor
        fields = [
            'user',
            'project',
            'role'
        ]
