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
    OWNER_ROLE = 'OWNER'
    CONTRIBUTOR_ROLE = 'CONTRIBUTOR'
    CREATOR_ROLE = 'CREATOR'
    
    ROLES = [
        (OWNER_ROLE, 'owner'),
        (CONTRIBUTOR_ROLE, 'contributor'),
        (CREATOR_ROLE, 'creator')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=256)
    role = models.CharField(max_length=256, choices=ROLES)
