from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from . import models
from authentication.models import User


class ProjectTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice',
                                             password='alice-password')

    def test_ok_create_project(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(reverse_lazy('issue_tracker:projects-list'), {
            'title': 'My Project',
            'description': 'This is my project',
            'type': 'IOS'
        })

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, models.Project.objects.count())
        project = models.Project.objects.all()[0]
        self.assertEqual(self.user, project.author)
        self.assertEqual('My Project', project.title)
        self.assertEqual('This is my project', project.description)
        self.assertEqual('IOS', project.type)

    def test_err_user_not_authenticated(self):
        client = APIClient()

        response = client.post(reverse_lazy('issue_tracker:projects-list'), {
            'title': 'My Project',
            'description': 'This is my project',
            'type': 'IOS'
        })

        self.assertNotEqual(200, response.status_code)
