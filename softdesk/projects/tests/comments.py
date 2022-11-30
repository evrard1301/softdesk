from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from rest_framework import status
from projects import models
from authentication.models import User


class CreateCommentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='bob',
            password='bob'
        )

        self.assignee = User.objects.create_user(
            username='dan',
            password='dan'
        )

        self.project = models.Project.objects.create(
            title='A Project',
            description='This is a project',
            type=models.Project.BACKEND_TYPE
        )

        self.issue = models.Issue.objects.create(
            title='my issue',
            description='this is my issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.user,
            assignee=self.assignee
        )

        self.issue_not_author = models.Issue.objects.create(
            title='my issue',
            description='this is my issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.assignee,
            assignee=self.assignee
        )

    def test_ok_collaborator(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.post(
            reverse_lazy(
                'projects:comments-list', kwargs={
                    'project_pk': self.project.id,
                    'issue_pk': self.issue.id
                }
            ), {
                'description': 'my comment',
                'author': self.user.id,
                'issue': self.issue.id
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        comment = models.Comment.objects.first()
        self.assertEqual('my comment', comment.description)
        self.assertEqual(self.user.id, comment.author.id)
        self.assertEqual(self.issue.id, comment.issue.id)

    def test_err_not_a_collaborator(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse_lazy(
                'projects:comments-list', kwargs={
                    'project_pk': self.project.id,
                    'issue_pk': self.issue.id
                }
            ), {
                'description': 'my comment',
                'author': self.user.id,
                'issue': self.issue.id
            }
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_authentificated(self):
        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.post(
            reverse_lazy(
                'projects:comments-list', kwargs={
                    'project_pk': self.project.id,
                    'issue_pk': self.issue.id
                }
            ), {
                'description': 'my comment',
                'author': self.user.id,
                'issue': self.issue.id
            }
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class UpdateCommentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='bob',
            password='bob'
        )

        self.assignee = User.objects.create_user(
            username='dan',
            password='dan'
        )

        self.project = models.Project.objects.create(
            title='A Project',
            description='This is a project',
            type=models.Project.BACKEND_TYPE
        )

        self.issue = models.Issue.objects.create(
            title='my issue',
            description='this is my issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.user,
            assignee=self.assignee
        )

        self.issue_not_author = models.Issue.objects.create(
            title='my issue',
            description='this is my issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.assignee,
            assignee=self.assignee
        )

        self.my_comment = models.Comment.objects.create(
            description='my comment',
            author=self.user,
            issue=self.issue
        )

        self.not_my_comment = models.Comment.objects.create(
            description='not my comment',
            author=self.assignee,
            issue=self.issue
        )

    def test_ok_collaborator(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.put(
            reverse_lazy(
                'projects:comments-detail', kwargs={
                    'project_pk': self.project.id,
                    'issue_pk': self.issue.id,
                    'pk': self.my_comment.id
                }
            ), {
                'description': 'my comment 2',
                'author': self.user.id,
                'issue': self.issue.id
            }
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        comment = models.Comment.objects.first()
        self.assertEqual('my comment 2', comment.description)
        self.assertEqual(self.user.id, comment.author.id)
        self.assertEqual(self.issue.id, comment.issue.id)

    def test_err_not_a_collaborator(self):
        self.client.force_authenticate(self.user)

        response = self.client.put(
            reverse_lazy(
                'projects:comments-detail', kwargs={
                    'project_pk': self.project.id,
                    'issue_pk': self.issue.id,
                    'pk': self.my_comment.id
                }
            ), {
                'description': 'my comment 2',
                'author': self.user.id,
                'issue': self.issue.id
            }
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_author(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.put(
            reverse_lazy(
                'projects:comments-detail', kwargs={
                    'project_pk': self.project.id,
                    'issue_pk': self.issue.id,
                    'pk': self.not_my_comment.id
                }
            ), {
                'description': 'my comment 2',
                'author': self.user.id,
                'issue': self.issue.id
            }
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_authentificated(self):
        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.put(
            reverse_lazy(
                'projects:comments-detail', kwargs={
                    'project_pk': self.project.id,
                    'issue_pk': self.issue.id,
                    'pk': self.my_comment.id
                }
            ), {
                'description': 'my comment 2',
                'author': self.user.id,
                'issue': self.issue.id
            }
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class DestroyCommentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='bob',
            password='bob'
        )

        self.assignee = User.objects.create_user(
            username='dan',
            password='dan'
        )

        self.project = models.Project.objects.create(
            title='A Project',
            description='This is a project',
            type=models.Project.BACKEND_TYPE
        )

        self.issue = models.Issue.objects.create(
            title='my issue',
            description='this is my issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.user,
            assignee=self.assignee
        )

        self.issue_not_author = models.Issue.objects.create(
            title='my issue',
            description='this is my issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.assignee,
            assignee=self.assignee
        )

        self.my_comment = models.Comment.objects.create(
            description='my comment',
            author=self.user,
            issue=self.issue
        )

        self.not_my_comment = models.Comment.objects.create(
            description='not my comment',
            author=self.assignee,
            issue=self.issue
        )

    def test_ok_collaborator(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.delete(
            reverse_lazy(
                'projects:comments-detail', kwargs={
                    'project_pk': self.project.id,
                    'issue_pk': self.issue.id,
                    'pk': self.my_comment.id
                }
            ))

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(
            0,
            models.Comment.objects.filter(id=self.my_comment.id).count()
        )

    def test_err_not_author(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.delete(
            reverse_lazy(
                'projects:comments-detail', kwargs={
                    'project_pk': self.project.id,
                    'issue_pk': self.issue.id,
                    'pk': self.not_my_comment.id
                }
            ))

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_authentificated(self):
        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.delete(
            reverse_lazy(
                'projects:comments-detail', kwargs={
                    'project_pk': self.project.id,
                    'issue_pk': self.issue.id,
                    'pk': self.my_comment.id
                }
            ))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class ListCommentsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='bob',
            password='bob'
        )

        self.assignee = User.objects.create_user(
            username='dan',
            password='dan'
        )

        self.project = models.Project.objects.create(
            title='A Project',
            description='This is a project',
            type=models.Project.BACKEND_TYPE
        )

        self.issue = models.Issue.objects.create(
            title='my issue',
            description='this is my issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.user,
            assignee=self.assignee
        )

        self.issue_not_author = models.Issue.objects.create(
            title='my issue',
            description='this is my issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.assignee,
            assignee=self.assignee
        )

        self.my_comments = []

        for i in range(0, 5):
            self.my_comments.append(models.Comment.objects.create(
                description=f'my comment {i}',
                author=self.user,
                issue=self.issue
            ))

        self.not_my_comment = models.Comment.objects.create(
            description='not my comment',
            author=self.assignee,
            issue=self.issue
        )

    def test_ok_collaborator(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.get(
            reverse_lazy('projects:comments-list', kwargs={
                'project_pk': self.project.id,
                'issue_pk': self.issue.id
            })
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(6, len(response.data))

    def test_err_not_collaborator(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse_lazy('projects:comments-list', kwargs={
                'project_pk': self.project.id,
                'issue_pk': self.issue.id
            })
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_authenticated(self):
        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.get(
            reverse_lazy('projects:comments-list', kwargs={
                'project_pk': self.project.id,
                'issue_pk': self.issue.id
            })
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class RetrieveCommentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='bob',
            password='bob'
        )

        self.assignee = User.objects.create_user(
            username='dan',
            password='dan'
        )

        self.project = models.Project.objects.create(
            title='A Project',
            description='This is a project',
            type=models.Project.BACKEND_TYPE
        )

        self.issue = models.Issue.objects.create(
            title='my issue',
            description='this is my issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.user,
            assignee=self.assignee
        )

        self.my_comments = []

        for i in range(0, 5):
            self.my_comments.append(models.Comment.objects.create(
                description=f'my comment {i}',
                author=self.user,
                issue=self.issue
            ))

    def test_ok_collaborator(self):
        self.client.force_authenticate(self.user)

        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.get(
            reverse_lazy('projects:comments-detail', kwargs={
                'project_pk': self.project.id,
                'issue_pk': self.issue.id,
                'pk': self.my_comments[0].id
            })
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('my comment 0', response.data['description'])

    def test_err_not_collaborator(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse_lazy('projects:comments-detail', kwargs={
                'project_pk': self.project.id,
                'issue_pk': self.issue.id,
                'pk': self.my_comments[0].id
            })
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
    
    def test_err_not_authenticated(self):
        models.Collaborator.objects.create(
            user=self.user,
            project=self.project,
            role=models.Collaborator.SUPERVISOR_ROLE
        )

        response = self.client.get(
            reverse_lazy('projects:comments-detail', kwargs={
                'project_pk': self.project.id,
                'issue_pk': self.issue.id,
                'pk': self.my_comments[0].id
            })
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

