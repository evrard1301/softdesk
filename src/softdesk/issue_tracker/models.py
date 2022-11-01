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

    author = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512, blank=True, null=True)
    type = models.CharField(max_length=128,
                            choices=PROJECT_TYPES,
                            default=BACK_END)
