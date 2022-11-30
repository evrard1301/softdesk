from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from rest_framework import status
from projects import models
from authentication.models import User


class CreateIssueTest(TestCase):
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

    def test_ok_as_author(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(
            user=self.user,
            project=self.project,
            role=models.Contributor.AUTHOR_ROLE
        )

        response = \
            self.client.post(reverse_lazy('projects:issues-list', kwargs={
                'project_pk': self.project.id
            }), {
                'title': 'my issue',
                'description': 'this is my issue',
                'tag': models.Issue.BUG_TAG,
                'priority': 1,
                'project': self.project.id,
                'status': models.Issue.OPEN_STATUS,
                'author': self.user.id,
                'assignee': self.assignee.id
            })

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, models.Issue.objects.count())
        issue = models.Issue.objects.all()[0];
        self.assertEqual('my issue', issue.title)
        self.assertEqual('this is my issue', issue.description)
        self.assertEqual(models.Issue.BUG_TAG, issue.tag)
        self.assertEqual(1, issue.priority)
        self.assertEqual(self.project.id, issue.project.id)
        self.assertEqual(models.Issue.OPEN_STATUS, issue.status)
        self.assertEqual(self.user.id, issue.author.id)
        self.assertEqual(self.assignee.id, issue.assignee.id)

    def test_ok_as_contributor(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(
            user=self.user,
            project=self.project,
            role=models.Contributor.CONTRIBUTOR_ROLE
        )

        response = \
            self.client.post(reverse_lazy('projects:issues-list', kwargs={
                'project_pk': self.project.id
            }), {
                'title': 'my issue',
                'description': 'this is my issue',
                'tag': models.Issue.BUG_TAG,
                'priority': 1,
                'project': self.project.id,
                'status': models.Issue.OPEN_STATUS,
                'author': self.user.id,
                'assignee': self.assignee.id
            })

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_err_not_a_collaborator(self):
        self.client.force_authenticate(self.user)

        response = \
            self.client.post(reverse_lazy('projects:issues-list', kwargs={
                'project_pk': self.project.id
            }), {
                'title': 'my issue',
                'description': 'this is my issue',
                'tag': models.Issue.BUG_TAG,
                'priority': 1,
                'project': self.project.id,
                'status': models.Issue.OPEN_STATUS,
                'author': self.user.id,
                'assignee': self.assignee.id
            })

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_autenticated(self):
        models.Contributor.objects.create(
            user=self.user,
            project=self.project,
            role=models.Contributor.CONTRIBUTOR_ROLE
        )

        response = \
            self.client.post(reverse_lazy('projects:issues-list', kwargs={
                'project_pk': self.project.id
            }), {
                'title': 'my issue',
                'description': 'this is my issue',
                'tag': models.Issue.BUG_TAG,
                'priority': 1,
                'project': self.project.id,
                'status': models.Issue.OPEN_STATUS,
                'author': self.user.id,
                'assignee': self.assignee.id
            })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class UpdateIssueTest(TestCase):
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

        self.issue2 = models.Issue.objects.create(
            title='my issue',
            description='this is my issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.assignee,
            assignee=self.assignee
        )

    def test_ok_as_author(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(
            user=self.user,
            project=self.project,
            role=models.Contributor.AUTHOR_ROLE
        )

        response = \
            self.client.put(reverse_lazy('projects:issues-detail', kwargs={
                'project_pk': self.project.id,
                'pk': self.issue.id
            }), {
                'title': 'my issue 2',
                'description': 'this is my issue 2',
                'tag': models.Issue.IMPROVEMENT_TAG,
                'priority': 4,
                'project': self.project.id,
                'status': models.Issue.CLOSED_STATUS,
                'author': self.assignee.id,
                'assignee': self.user.id
            })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        issue = models.Issue.objects.get(pk=self.issue.id)
        self.assertEqual('my issue 2', issue.title)
        self.assertEqual('this is my issue 2', issue.description)
        self.assertEqual(models.Issue.IMPROVEMENT_TAG, issue.tag)
        self.assertEqual(4, issue.priority)
        self.assertEqual(self.project.id, issue.project.id)
        self.assertEqual(models.Issue.CLOSED_STATUS, issue.status)
        self.assertEqual(self.user.id, issue.assignee.id)
        self.assertEqual(self.assignee.id, issue.author.id)

    def test_err_as_contributor(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(
            user=self.user,
            project=self.project,
            role=models.Contributor.CONTRIBUTOR_ROLE
        )

        response = \
            self.client.put(reverse_lazy('projects:issues-detail', kwargs={
                'project_pk': self.project.id,
                'pk': self.issue2.id
            }), {
                'title': 'my issue 2',
                'description': 'this is my issue 2',
                'tag': models.Issue.IMPROVEMENT_TAG,
                'priority': 4,
                'project': self.project.id,
                'status': models.Issue.CLOSED_STATUS,
                'author': self.assignee.id,
                'assignee': self.user.id
            })

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_a_collaborator(self):
        self.client.force_authenticate(self.user)

        response = \
            self.client.put(reverse_lazy('projects:issues-detail', kwargs={
                'project_pk': self.project.id,
                'pk': self.issue2.id
            }), {
                'title': 'my issue 2',
                'description': 'this is my issue 2',
                'tag': models.Issue.IMPROVEMENT_TAG,
                'priority': 4,
                'project': self.project.id,
                'status': models.Issue.CLOSED_STATUS,
                'author': self.assignee.id,
                'assignee': self.user.id
            })

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_autenticated(self):
        models.Contributor.objects.create(
            user=self.user,
            project=self.project,
            role=models.Contributor.AUTHOR_ROLE
        )

        response = \
            self.client.put(reverse_lazy('projects:issues-detail', kwargs={
                'project_pk': self.project.id,
                'pk': self.issue2.id
            }), {
                'title': 'my issue 2',
                'description': 'this is my issue 2',
                'tag': models.Issue.IMPROVEMENT_TAG,
                'priority': 4,
                'project': self.project.id,
                'status': models.Issue.CLOSED_STATUS,
                'author': self.assignee.id,
                'assignee': self.user.id
            })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class DestroyIssueTest(TestCase):
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
            title='your issue',
            description='not an author of this issue',
            tag=models.Issue.BUG_TAG,
            priority=1,
            project=self.project,
            status=models.Issue.OPEN_STATUS,
            author=self.assignee,
            assignee=self.assignee
        )

    def test_ok_as_author(self):
        self.client.force_authenticate(self.user)

        count = models.Issue.objects.count()

        response = self.client.delete(
            reverse_lazy('projects:issues-detail', kwargs={
                'pk': self.issue.id,
                'project_pk': self.project.id
            })
        )

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(count - 1, models.Issue.objects.count())

    def test_err_not_author(self):
        self.client.force_authenticate(self.user)

        count = models.Issue.objects.count()

        response = self.client.delete(
            reverse_lazy('projects:issues-detail', kwargs={
                'pk': self.issue_not_author.id,
                'project_pk': self.project.id
            })
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(count, models.Issue.objects.count())

    def test_err_not_authenticated(self):

        count = models.Issue.objects.count()

        response = self.client.delete(
            reverse_lazy('projects:issues-detail', kwargs={
                'pk': self.issue.id,
                'project_pk': self.project.id
            })
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(count, models.Issue.objects.count())


class ListIssuesTest(TestCase):
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

        self.issues = []

        for i in range(0, 3):
            self.issues.append(
                models.Issue.objects.create(
                    title=f'my issue{i}',
                    description='this is my issue',
                    tag=models.Issue.BUG_TAG,
                    priority=1,
                    project=self.project,
                    status=models.Issue.OPEN_STATUS,
                    author=self.user,
                    assignee=self.assignee
                )
            )

    def test_ok_collaborator(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(
            user=self.user,
            project=self.project,
            role=models.Contributor.CONTRIBUTOR_ROLE
        )

        response = self.client.get(reverse_lazy(
            'projects:issues-list', kwargs={
                'project_pk': self.project.id
            }))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))

    def test_err_not_a_collaborator(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse_lazy(
            'projects:issues-list', kwargs={
                'project_pk': self.project.id
            }))

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_authenticated(self):
        models.Contributor.objects.create(
            user=self.user,
            project=self.project,
            role=models.Contributor.CONTRIBUTOR_ROLE
        )

        response = self.client.get(reverse_lazy(
            'projects:issues-list', kwargs={
                'project_pk': self.project.id
            }))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


