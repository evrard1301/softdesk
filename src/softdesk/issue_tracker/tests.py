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
        self.bob = User.objects.create_user(username='bob',
                                            password='bob-password')
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

        models.Project.create_project(self.user, 'hello')
        models.Project.create_project(self.user, 'I love')
        models.Project.create_project(self.user, 'pizza')
        models.Project.create_project(self.bob, 'so much')
        
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
        models.Project.create_project(self.bob, 'hello')

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
        project = models.Project.create_project(self.bob, 'turing')

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
        project = models.Project.create_project(self.bob, 'alan')

        response = self.client.get(reverse_lazy('issue_tracker:projects-detail',
                                                args=[project.id]))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_show__not_authenticated(self):
        project = models.Project.create_project(self.user, 'manathan')

        response = self.client.get(reverse_lazy('issue_tracker:projects-detail',
                                                args=[project.id]))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ok_update(self):
        self.client.force_authenticate(self.user)

        project = models.Project.create_project(
            self.user,
            'my title',
            'my desc',
            models.Project.ANDROID
        )

        response = self.client.put(
            reverse_lazy('issue_tracker:projects-detail',
                         args=[project.id]), {
                             'title': 'new title',
                             'description': 'new description',
                             'type': models.Project.IOS
                         }
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        new_project = models.Project.objects.filter(pk=project.id).first()
        self.assertEqual('new title', new_project.title)
        self.assertEqual('new description', new_project.description)
        self.assertEqual(models.Project.IOS, new_project.type)

    def test_err_update__not_owner_but_contributor(self):
        self.client.force_authenticate(self.user)

        project = models.Project.create_project(
            self.bob,
            'my title',
            'my desc',
            models.Project.ANDROID
        )

        models.Contributor.objects.create(user=self.user, project=project)
        
        response = self.client.put(
            reverse_lazy('issue_tracker:projects-detail',
                         args=[project.id]), {
                             'title': 'new title',
                             'description': 'new description',
                             'type': models.Project.IOS
                         }
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        old_project = models.Project.objects.filter(pk=project.id).first()
        self.assertEqual('my title', old_project.title)
        self.assertEqual('my desc', old_project.description)
        self.assertEqual(models.Project.ANDROID, old_project.type)

    def test_ok_delete(self):
        self.client.force_authenticate(self.user)
        project = models.Project.create_project(self.user, 'my project')

        response = self.client.delete(
            reverse_lazy('issue_tracker:projects-detail',
                         args=[project.id])
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, models.Project.objects.count())
        
    def test_err_delete__not_owner_but_contributor(self):
        self.client.force_authenticate(self.user)
        project = models.Project.create_project(self.bob, 'my project')
        models.Contributor.objects.create(
            user=self.user,
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )
        response = self.client.delete(
            reverse_lazy('issue_tracker:projects-detail',
                         args=[project.id])
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, models.Project.objects.count())


class ContributorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice',
                                             password='alice-password')
        self.bob = User.objects.create_user(username='bob',
                                            password='bob-password')
        self.client = APIClient()
        
    def test_ok_add_contributor(self):
        self.client.force_authenticate(self.user)

        project = models.Project.create_project(self.user, 'project')

        self.assertEqual(
            0,
            models.Contributor.objects.filter(user=self.bob,
                                              project=project).count()
        )
        
        response = self.client.post(reverse_lazy(
            'issue_tracker:contributors-list',
            args=[project.id]), {
                'user_id': self.bob.id
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(
            1,
            models.Contributor.objects.filter(user=self.bob,
                                              project=project).count()
        )

    def test_err_add_contributor__not_owner(self):
        self.client.force_authenticate(self.user)

        project = models.Project.create_project(self.bob, 'project')
        
        response = self.client.post(reverse_lazy(
            'issue_tracker:contributors-list',
            args=[project.id]), {
                'user_id': self.user.id
        })

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ok_list_contributors(self):
        self.client.force_authenticate(self.user)

        project = models.Project.create_project(self.user, 'proj 0')

        models.Contributor.objects.create(
            user=User.objects.create_user(username='claire', password='nop'),
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )

        models.Contributor.objects.create(
            user=User.objects.create_user(username='dan', password='nop'),
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )

        models.Contributor.objects.create(
            user=User.objects.create_user(username='edward', password='nop'),
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )

        response = self.client.get(
            reverse_lazy('issue_tracker:contributors-list', args=[project.id])
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(4, len(response.data))
        self.assertEqual('alice', response.data[0]['username'])
        self.assertEqual('claire', response.data[1]['username'])
        self.assertEqual('dan', response.data[2]['username'])
        self.assertEqual('edward', response.data[3]['username'])

    def test_ok_list_contributors__contributor(self):
        self.client.force_authenticate(self.user)

        project = models.Project.create_project(self.bob, 'proj 0')

        models.Contributor.objects.create(
            user=User.objects.create_user(username='claire', password='nop'),
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )

        models.Contributor.objects.create(
            user=self.user,
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )

        response = self.client.get(
            reverse_lazy('issue_tracker:contributors-list', args=[project.id])
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
        self.assertEqual('bob', response.data[0]['username'])
        self.assertEqual('claire', response.data[1]['username'])
        self.assertEqual('alice', response.data[2]['username'])

    def test_err_list_contributors__not_contributor(self):
        self.client.force_authenticate(self.user)

        project = models.Project.create_project(self.bob, 'proj 0')

        models.Contributor.objects.create(
            user=User.objects.create_user(username='claire', password='nop'),
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )

        response = self.client.get(
            reverse_lazy('issue_tracker:contributors-list', args=[project.id])
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ok_delete_contributor(self):
        self.client.force_authenticate(self.user)
        project = models.Project.create_project(self.user, 'project')

        models.Contributor.objects.create(
            user=self.bob,
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )

        self.assertEqual(
            1,
            models.Contributor.objects.filter(
                project=project,
                user=self.bob
            ).count()
        )
        
        response = self.client.delete(
            reverse_lazy(
                'issue_tracker:contributors-detail',
                args=[
                    project.id,
                    self.bob.id
                ]
            )
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            0,
            models.Contributor.objects.filter(
                project=project,
                user=self.bob
            ).count()
        )

    def test_err_delete_contributor__only_teammate(self):
        self.client.force_authenticate(self.user)
        project = models.Project.create_project(self.bob, 'project')

        models.Contributor.objects.create(
            user=self.bob,
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )

        models.Contributor.objects.create(
            user=self.user,
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )

        response = self.client.delete(
            reverse_lazy(
                'issue_tracker:contributors-detail',
                args=[
                    project.id,
                    self.bob.id
                ]
            )
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_delete_contributor__not_contributor(self):
        self.client.force_authenticate(self.user)
        project = models.Project.create_project(self.bob, 'project')

        models.Contributor.objects.create(
            user=self.bob,
            project=project,
            role=models.Contributor.ROLE_TEAMMATE
        )

        response = self.client.delete(
            reverse_lazy(
                'issue_tracker:contributors-detail',
                args=[
                    project.id,
                    self.bob.id
                ]
            )
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
