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

    def test_ok_query_list(self):
        models.Project.objects.create(author=self.user,
                                      title='project 1',
                                      description='my first project',
                                      type=models.Project.BACK_END)

        models.Project.objects.create(author=self.user,
                                      title='project 2',
                                      description='my second project',
                                      type=models.Project.BACK_END)

        models.Project.objects.create(author=self.user,
                                      title='project 3',
                                      description='my third project',
                                      type=models.Project.BACK_END)

        bob = User.objects.create_user(username='bob', password='bobbobbob')
        models.Project.objects.create(author=bob,
                                      title='project 4',
                                      description='bob\'s project',
                                      type=models.Project.BACK_END)

        client = APIClient()
        client.force_authenticate(self.user)

        response = client.get(reverse_lazy('issue_tracker:projects-list'))

        self.assertEqual(200, response.status_code)

        self.assertEqual(3, len(response.data))
        self.assertEqual('project 1', response.data[0]['title'])
        self.assertEqual('project 2', response.data[1]['title'])
        self.assertEqual('project 3', response.data[2]['title'])

    def test_err_query_list_not_authenticated(self):
        client = APIClient()
        response = client.get(reverse_lazy('issue_tracker:projects-list'))
        self.assertNotEqual(200, response.status_code)
