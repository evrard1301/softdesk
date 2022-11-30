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

urlpatterns = [
    path('', include(projects.urls)),
    path('', include(users.urls)),
]
