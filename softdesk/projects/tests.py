from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from rest_framework import status
from . import models
from authentication.models import User


class CreateProjectTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('alice', 'azerty')
        
    def test_ok(self):
        self.client.force_authenticate(self.user)
        
        response = self.client.post(reverse_lazy('projects:projects-list'), {
            'title': 'My project',
            'description': 'this is my project',
            'type': models.Project.ANDROID_TYPE
        })

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        project = models.Project.objects.all()[0]
        self.assertEqual('My project', project.title)
        self.assertEqual('this is my project', project.description)
        self.assertEqual(models.Project.ANDROID_TYPE, project.type)

    def test_err_not_authenticated(self):
        response = self.client.post(reverse_lazy('projects:projects-list'), {
            'title': 'My project',
            'description': 'this is my project',
            'type': models.Project.ANDROID_TYPE
        })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
