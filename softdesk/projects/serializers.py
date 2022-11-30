from rest_framework.serializers import ModelSerializer
from . import models
from rest_framework import serializers


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


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = [
            'title', 'description',
            'tag', 'priority',
            'project', 'status',
            'author', 'assignee',
            'created'
        ]
