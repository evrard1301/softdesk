from django.urls import path, include
from rest_framework_nested import routers
from . import views

app_name = 'projects'

projects = routers.SimpleRouter()
projects.register('projects', views.ProjectView, basename='projects')

users = routers.NestedSimpleRouter(projects, 'projects',
                                   lookup='project')
users.register('users',
               views.UserView,
               basename='users')

issues = routers.NestedSimpleRouter(projects, 'projects', lookup='project')
issues.register('issues', views.IssueView, basename='issues')

comments = routers.NestedSimpleRouter(issues, 'issues', lookup='issue')
comments.register('comments', views.CommentView, basename='comments')

urlpatterns = [
    path('', include(projects.urls)),
    path('', include(users.urls)),
    path('', include(issues.urls)),
    path('', include(comments.urls)),
]
