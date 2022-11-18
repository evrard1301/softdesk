from django.db import models
from authentication import models as auth_models


class Project(models.Model):
    BACK_END = 'BE'
    FRONT_END = 'FE'
    IOS = 'IOS'
    ANDROID = 'AN'

    PROJECT_TYPES = [
        (BACK_END, 'back-end'),
        (FRONT_END, 'front-end'),
        (IOS, 'IOS'),
        (ANDROID, 'Android')
    ]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512, blank=True, null=True)
    type = models.CharField(max_length=128,
                            choices=PROJECT_TYPES,
                            default=BACK_END)

    def create_project(owner, title, description='', type=BACK_END):
        proj = Project.objects.create(title=title, description=description,
                                      type=type)
        Contributor.objects.create(project=proj,
                                   user=owner,
                                   role=Contributor.ROLE_OWNER)
        return proj

    
class Contributor(models.Model):
    ROLE_OWNER = 'OWNER'
    ROLE_TEAMMATE = 'TEAM_MATE'
    
    CONTRIBUTOR_ROLES = [
        (ROLE_OWNER, 'owner'),
        (ROLE_TEAMMATE, 'teammate')
    ]
    
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=256,
                            choices=CONTRIBUTOR_ROLES,
                            default=ROLE_TEAMMATE)
    
