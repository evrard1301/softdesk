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

    def test_ok_create_project(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(reverse_lazy('issue_tracker:projects-list'), {
            'title': 'My Project',
            'description': 'This is my project',
            'type': 'IOS'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, models.Project.objects.count())
        project = models.Project.objects.all()[0]
        
        contrib = models.Contributor.objects.filter(user=self.user, project=project).first()
        self.assertEqual(models.Contributor.ROLE_OWNER, contrib.role)
        
        self.assertEqual('My Project', project.title)
        self.assertEqual('This is my project', project.description)
        self.assertEqual('IOS', project.type)

    def test_err_create_project_not_authenticated(self):
        client = APIClient()

        response = client.post(reverse_lazy('issue_tracker:projects-list'), {
            'title': 'My Project',
            'description': 'This is my project',
            'type': 'IOS'
        })

        self.assertNotEqual(status.HTTP_200_OK, response.status_code)

    def test_ok_add_contributor(self):
        client = APIClient()
        client.force_authenticate(self.user)
        contributor = User.objects.create_user(username='bob',
                                               password='bob-password')
        
        project = \
            models.Project.create_project(self.user,
                                          title='My awesome project',
                                          description='aaaaaawesome',
                                          type=models.Project.BACK_END)        

        contributors = models.Contributor.objects.filter(project=project)
        self.assertEqual(1, len(contributors))
        
        client.post(reverse_lazy('issue_tracker:contributor',
                                 args=[project.id]), {
            'user_id': contributor.id
        })
        
        contributors = models.Contributor.objects.filter(project=project)
        self.assertEqual(2, len(contributors))
        self.assertEqual(contributor.id, contributors[1].user.id)

    def test_err_add_contributor_already_added(self):
        client = APIClient()
        client.force_authenticate(self.user)
        contributor = User.objects.create_user(username='bob',
                                               password='bob-password')
        
        project = \
            models.Project.create_project(self.user,
                                          title='My awesome project',
                                          description='aaaaaawesome',
                                          type=models.Project.BACK_END)
        
        project.save()

        models.Contributor.objects.create(user=contributor, project=project)
                
        response = client.post(reverse_lazy('issue_tracker:contributor',
                                            args=[project.id]), {
            'user_id': contributor.id
        })
        
        contributors = models.Contributor.objects.filter(project=project)
        self.assertEqual(2, len(contributors))
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)

    def test_err_add_contributor_not_authenticated(self):
        client = APIClient()
        contributor = User.objects.create_user(username='bob',
                                               password='bob-password')
        
        project = \
            models.Project.create_project(self.user,
                                                  title='My awesome project',
                                                  description='aaaaaawesome',
                                                  type=models.Project.BACK_END)
        
        project.save()

        contributors = models.Contributor.objects.filter(project=project)
        self.assertEqual(1, len(contributors))
        
        response = client.post(reverse_lazy('issue_tracker:contributor',
                                            args=[project.id]), {
            'user_id': contributor.id
        })
        
        contributors = models.Contributor.objects.filter(project=project)
        self.assertEqual(1, len(contributors))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_err_add_contributor_not_project_owner(self):
        client = APIClient()
        client.force_authenticate(self.user)
        owner = User.objects.create_user(username='claire',
                                         password='claire-password')

        contributor = User.objects.create_user(username='bob',
                                               password='bob-password')
        
        project = \
            models.Project.create_project(owner,
                                          title='My awesome project',
                                          description='aaaaaawesome',
                                          type=models.Project.BACK_END)
        
        project.save()

        contributors = models.Contributor.objects.filter(project=project)
        self.assertEqual(1, len(contributors))
        
        response = client.post(reverse_lazy('issue_tracker:contributor',
                                            args=[project.id]), {
                                            'user_id': contributor.id
        })
        
        contributors = models.Contributor.objects.filter(project=project)
        self.assertEqual(1, len(contributors))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ok_list_contributors_by_owner(self):
        client = APIClient()
        bob = User.objects.create_user(username='bob', password='aze')
        claire = User.objects.create_user(username='claire', password='aze')
        dan = User.objects.create_user(username='dan', password='aze')
        User.objects.create_user(username='evarist', password='aze')
        User.objects.create_user(username='frank', password='aze')
        
        project = \
            models.Project.create_project(self.user,
                                                  title='My awesome project',
                                                  description='aaaaaawesome',
                                                  type=models.Project.BACK_END)
        project.save()
        
        client.force_authenticate(self.user)
        
        models.Contributor.objects.create(user=bob, project=project)
        models.Contributor.objects.create(user=claire, project=project)
        models.Contributor.objects.create(user=dan, project=project)

        response = client.get(reverse_lazy('issue_tracker:contributor',
                                           args=[project.id]))
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(4, len(response.data))
        self.assertEqual(self.user.username, response.data[0]['username'])
        self.assertEqual('bob', response.data[1]['username'])
        self.assertEqual('claire', response.data[2]['username'])
        self.assertEqual('dan', response.data[3]['username'])
        
    def test_ok_list_contributors_by_contributor(self):
        client = APIClient()
        bob = User.objects.create_user(username='bob', password='aze')
        claire = User.objects.create_user(username='claire', password='aze')
        dan = User.objects.create_user(username='dan', password='aze')
        User.objects.create_user(username='evarist', password='aze')
        User.objects.create_user(username='frank', password='aze')
        
        project = \
            models.Project.create_project(bob,
                                                  title='My awesome project',
                                                  description='aaaaaawesome',
                                                  type=models.Project.BACK_END)
        project.save()
        
        client.force_authenticate(self.user)
        
        models.Contributor.objects.create(user=self.user, project=project)
        models.Contributor.objects.create(user=claire, project=project)
        models.Contributor.objects.create(user=dan, project=project)

        response = client.get(reverse_lazy('issue_tracker:contributor',
                                           args=[project.id]))
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(4, len(response.data))
        self.assertEqual('bob', response.data[0]['username'])
        self.assertEqual(self.user.username, response.data[1]['username'])
        self.assertEqual('claire', response.data[2]['username'])
        self.assertEqual('dan', response.data[3]['username'])
        
    def test_err_list_contributors_not_authenticated(self):
        client = APIClient()
        bob = User.objects.create_user(username='bob', password='aze')
        
        project = \
            models.Project.create_project(self.user,
                                          title='My awesome project',
                                          description='aaaaaawesome',
                                          type=models.Project.BACK_END)
        project.save()
        
        models.Contributor.objects.create(user=bob, project=project)

        response = client.get(reverse_lazy('issue_tracker:contributor',
                                           args=[project.id]))
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_err_list_contributors_not_contributor(self):
        client = APIClient()
        bob = User.objects.create_user(username='bob', password='aze')
        
        project = \
            models.Project.create_project(bob,
                                          title='My awesome project',
                                          description='aaaaaawesome',
                                          type=models.Project.BACK_END)
        project.save()
        client.force_authenticate(self.user)

        response = client.get(reverse_lazy('issue_tracker:contributor',
                                           args=[project.id]))
        
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
