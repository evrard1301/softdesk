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

        contribs = models.Contributor.objects.filter(user=self.user,
                                                    project=project)
        self.assertEqual(1, contribs.count())
        self.assertEqual(models.Contributor.AUTHOR_ROLE, contribs[0].role)
        
    def test_err_not_authenticated(self):
        response = self.client.post(reverse_lazy('projects:projects-list'), {
            'title': 'My project',
            'description': 'this is my project',
            'type': models.Project.ANDROID_TYPE
        })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        
class UpdateProjectTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('alice', 'azerty')
        self.project = \
            models.Project.objects.create(title='Project 0',
                                          description='random stuff',
                                          type=models.Project.IOS_TYPE)

    def test_ok(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.AUTHOR_ROLE)
        response = self.client.put(
            reverse_lazy('projects:projects-detail', args=[self.project.id]), {
                'title': 'My updated project',
                'description': 'this is my updated project',
                'type': models.Project.ANDROID_TYPE
            })        
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        project = models.Project.objects.get(pk=self.project.id)
        self.assertEqual('My updated project', project.title)
        self.assertEqual('this is my updated project', project.description)
        self.assertEqual(models.Project.ANDROID_TYPE, project.type)

    def test_err_not_authenticated(self):
        response = self.client.put(
            reverse_lazy('projects:projects-detail', args=[self.project.id]), {
                'title': 'My updated project',
                'description': 'this is my updated project',
                'type': models.Project.ANDROID_TYPE
            })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_err_not_author(self):
        self.client.force_authenticate(self.user)
        
        response = self.client.put(
            reverse_lazy('projects:projects-detail', args=[self.project.id]), {
                'title': 'My updated project',
                'description': 'this is my updated project',
                'type': models.Project.ANDROID_TYPE
            })
        
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_author_but_supervisor(self):
        self.client.force_authenticate(self.user)
        
        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.
                                          SUPERVISOR_ROLE)
        
        response = self.client.put(
            reverse_lazy('projects:projects-detail', args=[self.project.id]), {
                'title': 'My updated project',
                'description': 'this is my updated project',
                'type': models.Project.ANDROID_TYPE
            })
        
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        
class DeleteProjectTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('alice', 'azerty')
        self.project = \
            models.Project.objects.create(title='Project 0',
                                          description='random stuff',
                                          type=models.Project.IOS_TYPE)

    def test_ok(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.AUTHOR_ROLE)
        response = self.client.delete(
            reverse_lazy('projects:projects-detail', args=[self.project.id])
        )
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        self.assertEqual(
            0,
            models.Project.objects.filter(pk=self.project.id).count()
        )

    def test_err_not_authenticated(self):
        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.AUTHOR_ROLE)
        response = self.client.delete(
            reverse_lazy('projects:projects-detail', args=[self.project.id])
        )
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_err_not_author(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse_lazy('projects:projects-detail', args=[self.project.id])
        )
        
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_err_not_author_but_supervisor(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.SUPERVISOR_ROLE)
        response = self.client.delete(
            reverse_lazy('projects:projects-detail', args=[self.project.id])
        )
        
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class ListProjectsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('alice', 'azerty')
        self.projects = [
            models.Project.objects.create(title='Project 0',
                                          description='random stuff',
                                          type=models.Project.FRONTEND_TYPE),
            models.Project.objects.create(title='Project 1',
                                          description='random stuff',
                                          type=models.Project.BACKEND_TYPE),
            models.Project.objects.create(title='Project 2',
                                          description='random stuff',
                                          type=models.Project.ANDROID_TYPE)
        ]

    def test_ok_related_to_all_projects(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(
            user=self.user,
            project=self.projects[0],
            role=models.Contributor.AUTHOR_ROLE
        )

        models.Contributor.objects.create(
            user=self.user,
            project=self.projects[1],
            role=models.Contributor.SUPERVISOR_ROLE
        )

        models.Contributor.objects.create(
            user=self.user,
            project=self.projects[2],
            role=models.Contributor.CONTRIBUTOR_ROLE
        )

        response = self.client.get(
            reverse_lazy('projects:projects-list')
        )
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
        
    def test_ok_related_to_one_project(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(
            user=self.user,
            project=self.projects[1],
            role=models.Contributor.CONTRIBUTOR_ROLE
        )

        response = self.client.get(
            reverse_lazy('projects:projects-list')
        )
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual('Project 1', response.data[0].get('title'))

    def test_ok_not_related_to_any_project(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse_lazy('projects:projects-list')
        )
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, len(response.data))
        
    def test_err_not_authenticated(self):
        response = self.client.get(
            reverse_lazy('projects:projects-list')
        )
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class ListProjectTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('alice', 'azerty')
        self.projects = [
            models.Project.objects.create(title='Project 0',
                                          description='random stuff',
                                          type=models.Project.FRONTEND_TYPE),
            models.Project.objects.create(title='Project 1',
                                          description='random stuff',
                                          type=models.Project.BACKEND_TYPE),
            models.Project.objects.create(title='Project 2',
                                          description='random stuff',
                                          type=models.Project.ANDROID_TYPE)
        ]

    def test_ok_related_to_the_project(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(
            user=self.user,
            project=self.projects[2],
            role=models.Contributor.CONTRIBUTOR_ROLE
        )

        response = self.client.get(
            reverse_lazy('projects:projects-detail',
                         args=[self.projects[2].id])
        )
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Project 2', response.data.get('title'))
        
    def test_ok_not_related_to_the_project(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse_lazy('projects:projects-detail', args=[self.projects[1].id])
        )
        
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        
    def test_err_not_authenticated(self):
        response = self.client.get(
            reverse_lazy('projects:projects-detail', args=[self.projects[0].id])
        )
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


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

        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.AUTHOR_ROLE)
        
        num_contrib = models.Contributor.objects.filter(user=self.user).count()
        
        response = self.client.post(
            reverse_lazy('projects:users-list', kwargs={'project_pk':
                                                        self.project.id}), {
                'user': self.user.id,
                'role': models.Contributor.SUPERVISOR_ROLE
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(
            num_contrib + 1,
            models.Contributor.objects.filter(user=self.user).count()
        )

    def test_ko_not_project_author(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse_lazy('projects:users-list', kwargs={'project_pk':
                                                        self.project.id}), {
                'user': self.user.id,
                'role': models.Contributor.SUPERVISOR_ROLE
            }
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ko_not_project_author_but_supervisor(self):
        self.client.force_authenticate(self.user)
        
        models.Contributor.objects.create(
            user=self.user,
            project=self.project,
            role=models.Contributor.SUPERVISOR_ROLE
        )

        response = self.client.post(
            reverse_lazy('projects:users-list', kwargs={'project_pk':
                                                        self.project.id}), {
                'user': self.user.id,
                'role': models.Contributor.SUPERVISOR_ROLE
            }
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ko_not_authenticated(self):

        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.AUTHOR_ROLE)

        response = self.client.post(
            reverse_lazy('projects:users-list', kwargs={'project_pk':
                                                        self.project.id}), {
                'user': self.user.id,
                'role': models.Contributor.SUPERVISOR_ROLE
            }
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        
class DeleteCollaboratorTest(TestCase):
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

        models.Contributor.objects.create(
            user=self.collaborator,
            project=self.project,
            role=models.Contributor.CONTRIBUTOR_ROLE
        )
        
    def test_ok(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.AUTHOR_ROLE)                
        
        response = self.client.delete(
            reverse_lazy('projects:users-detail',
                         kwargs={'project_pk': self.project.id,
                                 'pk': self.collaborator.id})
        )

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(
            0,
            models.Contributor.objects.filter(user=self.collaborator).count()
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

        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.SUPERVISOR_ROLE)                
        
        response = self.client.delete(
            reverse_lazy('projects:users-detail',
                         kwargs={'project_pk': self.project.id,
                                 'pk': self.collaborator.id})
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ko_not_authenticated(self):

        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.AUTHOR_ROLE)                
        
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

        models.Contributor.objects.create(
            user=self.collaborators[0],
            project=self.project,
            role=models.Contributor.CONTRIBUTOR_ROLE
        )

        models.Contributor.objects.create(
            user=self.collaborators[1],
            project=self.project,
            role=models.Contributor.SUPERVISOR_ROLE
        )
        
    def test_ok_author(self):
        self.client.force_authenticate(self.user)

        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.AUTHOR_ROLE)                
        
        response = self.client.get(reverse_lazy('projects:users-list', kwargs={
            'project_pk': self.project.id
        }))        

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))

    def test_ok_collaborator(self):
        self.client.force_authenticate(self.user)
      
        models.Contributor.objects.create(
            user=self.user,
            project=self.project,
            role=models.Contributor.SUPERVISOR_ROLE
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
        models.Contributor.objects.create(user=self.user,
                                          project=self.project,
                                          role=models.Contributor.AUTHOR_ROLE)                
      
        response = self.client.get(reverse_lazy('projects:users-list', kwargs={
            'project_pk': self.project.id
        }))        
  
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        
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
