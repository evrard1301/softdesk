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


class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collaborator
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            'description',
            'author',
            'issue',
            'created'
        ]
