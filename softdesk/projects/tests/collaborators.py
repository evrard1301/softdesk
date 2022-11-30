from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from rest_framework import status
from projects import models
from authentication.models import User


class CreateCollaboratorTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='bob',
                                             password='coucou')
        self.project = models.Project.objects.create(
            title='my project',
            description='',
            type=models.Project.BACKEND_TYPE
        )

    def test_ok(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Collaborator.AUTHOR_ROLE)

        num_contrib = models.Collaborator.objects.filter(user=self.user).count()

        response = self.client.post(
            reverse_lazy('projects:users-list', kwargs={'project_pk':
                                                        self.project.id}), {
                'user': self.user.id,
                'role': models.Collaborator.SUPERVISOR_ROLE
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(
            num_contrib + 1,
            models.Collaborator.objects.filter(user=self.user).count()
        )

    def test_ko_not_project_author(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse_lazy('projects:users-list', kwargs={'project_pk':
                                                        self.project.id}), {
                'user': self.user.id,
                'role': models.Collaborator.SUPERVISOR_ROLE
            }
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ko_not_project_author_but_supervisor(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.post(
            reverse_lazy('projects:users-list', kwargs={'project_pk':
                                                        self.project.id}), {
                'user': self.user.id,
                'role': models.Collaborator.SUPERVISOR_ROLE
            }
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ko_not_authenticated(self):

        models.Collaborator.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Collaborator.AUTHOR_ROLE)

        response = self.client.post(
            reverse_lazy('projects:users-list', kwargs={'project_pk':
                                                        self.project.id}), {
                'user': self.user.id,
                'role': models.Collaborator.SUPERVISOR_ROLE
            }
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class DestroyCollaboratorTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='bob',
                                             password='coucou')

        self.collaborator = User.objects.create_user(username='sam',
                                                     password='hello')

        self.project = models.Project.objects.create(
            title='my project',
            description='',
            type=models.Project.BACKEND_TYPE
        )

        models.Collaborator.objects.create(
            user=self.collaborator,
            project=self.project,
            role=models.Collaborator.CONTRIBUTOR_ROLE
        )

    def test_ok(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Collaborator.AUTHOR_ROLE)

        response = self.client.delete(
            reverse_lazy('projects:users-detail',
                         kwargs={'project_pk': self.project.id,
                                 'pk': self.collaborator.id})
        )

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(
            0,
            models.Collaborator.objects.filter(user=self.collaborator).count()
        )

    def test_ko_not_project_author(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse_lazy('projects:users-detail',
                         kwargs={'project_pk': self.project.id,
                                 'pk': self.collaborator.id})
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ko_not_project_author_but_supervisor(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Collaborator.SUPERVISOR_ROLE)

        response = self.client.delete(
            reverse_lazy('projects:users-detail',
                         kwargs={'project_pk': self.project.id,
                                 'pk': self.collaborator.id})
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ko_not_authenticated(self):

        models.Collaborator.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Collaborator.AUTHOR_ROLE)

        response = self.client.delete(
            reverse_lazy('projects:users-detail',
                         kwargs={'project_pk': self.project.id,
                                 'pk': self.collaborator.id})
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class ListCollaboratorsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='bob',
                                             password='coucou')

        self.collaborators = [
            User.objects.create_user(username='sam',
                                     password='hello'),
            User.objects.create_user(username='tim',
                                     password='hello aussi')
        ]

        self.project = models.Project.objects.create(
            title='my project',
            description='',
            type=models.Project.BACKEND_TYPE
        )

        models.Collaborator.objects.create(
            user=self.collaborators[0],
            project=self.project,
            role=models.Collaborator.CONTRIBUTOR_ROLE
        )

        models.Collaborator.objects.create(
            user=self.collaborators[1],
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

    def test_ok_author(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Collaborator.AUTHOR_ROLE)

        response = self.client.get(reverse_lazy('projects:users-list', kwargs={
            'project_pk': self.project.id
        }))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))

    def test_ok_collaborator(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.get(reverse_lazy('projects:users-list', kwargs={
            'project_pk': self.project.id
        }))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))

    def test_ko_not_project_author(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse_lazy('projects:users-list', kwargs={
            'project_pk': self.project.id
        }))

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ko_not_authenticated(self):
        models.Collaborator.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Collaborator.AUTHOR_ROLE)

        response = self.client.get(reverse_lazy('projects:users-list', kwargs={
            'project_pk': self.project.id
        }))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
