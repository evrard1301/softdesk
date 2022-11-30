from django.db import models
from authentication.models import User


class Project(models.Model):
    ANDROID_TYPE = 'ANDROID'
    IOS_TYPE = 'IOS'
    BACKEND_TYPE = 'BACKEND'
    FRONTEND_TYPE = 'FRONTEND'
    
    TYPES = [
        (ANDROID_TYPE, 'Android'),
        (IOS_TYPE, 'IOS'),
        (BACKEND_TYPE, 'Back-end'),
        (FRONTEND_TYPE, 'Front-End')
    ]
    
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=4096)
    type = models.CharField(max_length=64, choices=TYPES)


class Contributor(models.Model):
    SUPERVISOR_ROLE = 'SUPERVISOR'
    CONTRIBUTOR_ROLE = 'CONTRIBUTOR'
    AUTHOR_ROLE = 'AUTHOR'
    
    ROLES = [
        (SUPERVISOR_ROLE, 'supervisor'),
        (CONTRIBUTOR_ROLE, 'contributor'),
        (AUTHOR_ROLE, 'author')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=256, choices=ROLES)


class Issue(models.Model):
    BUG_TAG = 'BUG'
    IMPROVEMENT_TAG = 'IMPROVEMENT'
    TASK_TAG = 'TASK'
    
    TAGS = [
        (BUG_TAG, 'bug'),
        (IMPROVEMENT_TAG, 'improvement'),
        (TASK_TAG, 'task')
    ]

    OPEN_STATUS = 'OPEN'
    CLOSED_STATUS = 'CLOSED'
    
    STATUS = [
        (OPEN_STATUS, 'open'),
        (CLOSED_STATUS, 'closed')
    ]
    
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=4096)
    tag = models.CharField(max_length=128, choices=TAGS)
    priority = models.IntegerField()
    status = models.CharField(max_length=128, choices=STATUS)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assignee'
    )
    created = models.DateTimeField(auto_now=True)
    

class Comment(models.Model):
    description = models.CharField(max_length=4096)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
