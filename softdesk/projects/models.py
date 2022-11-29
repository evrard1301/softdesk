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
