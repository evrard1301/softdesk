from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from rest_framework import status
from . import models
from authentication.models import User


class ProjectTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice',
                                             password='alice-password')
        self.client = APIClient()
        
    def test_ok_create(self):        
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse_lazy('issue_tracker:projects-list'), {
            'title': 'My Project',
            'description': 'This is my project',
            'type': 'IOS'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, models.Project.objects.count())
        project = models.Project.objects.all()[0]
        
        contrib = models.Contributor.objects.filter(user=self.user,
                                                    project=project).first()
        self.assertIsNotNone(contrib)
        self.assertEqual(models.Contributor.ROLE_OWNER, contrib.role)
        
        self.assertEqual('My Project', project.title)
        self.assertEqual('This is my project', project.description)
        self.assertEqual('IOS', project.type)

    def test_err_create__not_authenticated(self):
        before = models.Project.objects.count()
        
        response = self.client.post(reverse_lazy('issue_tracker:projects-list'), {
            'title': 'My Project',
            'description': 'This is my project',
            'type': 'IOS'
        })

        self.assertEqual(before, models.Project.objects.count())
        self.assertNotEqual(status.HTTP_200_OK, response.status_code)
