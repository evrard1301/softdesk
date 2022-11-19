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

    def test_ok_list__owner(self):
        self.client.force_authenticate(self.user)
        bob = User.objects.create_user(username='bob', password='azerty')
        models.Project.create_project(self.user, 'hello')
        models.Project.create_project(self.user, 'I love')
        models.Project.create_project(self.user, 'pizza')
        models.Project.create_project(bob, 'so much')
        
        response = self.client.get(reverse_lazy('issue_tracker:projects-list'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
        self.assertEqual('hello', response.data[0]['title'])
        self.assertEqual('I love', response.data[1]['title'])
        self.assertEqual('pizza', response.data[2]['title'])
        
    def test_err_list__not_authenticated(self):
        response = self.client.get(reverse_lazy('issue_tracker:projects-list'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_err_list__not_contributor(self):
        self.client.force_authenticate(self.user)
        bob = User.objects.create_user(username='bob', password='azerty')
        models.Project.create_project(bob, 'hello')

        response = self.client.get(reverse_lazy('issue_tracker:projects-list'))
        self.assertEqual(0, len(response.data))

    def test_ok_show(self):
        self.client.force_authenticate(self.user)
        project = models.Project.create_project(self.user, 'turing')
        
        response = \
            self.client.get(reverse_lazy('issue_tracker:projects-detail',
                                         args=[project.id]))
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('turing', response.data['title'])

    def test_ok_show__not_the_owner(self):
        self.client.force_authenticate(self.user)
        bob = User.objects.create_user(username='bob', password='azerty')
        project = models.Project.create_project(bob, 'turing')

        models.Contributor.objects.create(
            user=self.user,
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )
        
        response = \
            self.client.get(reverse_lazy('issue_tracker:projects-detail',
                                         args=[project.id]))
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('turing', response.data['title'])
    
    def test_err_show__not_a_contributor(self):
        self.client.force_authenticate(self.user)
        bob = User.objects.create_user(username='bob', password='azerty')
        project = models.Project.create_project(bob, 'alan')

        response = self.client.get(reverse_lazy('issue_tracker:projects-detail',
                                                args=[project.id]))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_show__not_authenticated(self):
        project = models.Project.create_project(self.user, 'manathan')

        response = self.client.get(reverse_lazy('issue_tracker:projects-detail',
                                                args=[project.id]))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

