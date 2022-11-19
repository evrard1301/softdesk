from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter
from . import views

app_name = 'issue_tracker'

projects_router = routers.DefaultRouter()
projects_router.register('projects', views.ProjectViewSet, basename='projects')

contributors_router = NestedSimpleRouter(projects_router,
                                         'projects',
                                         lookup='project')

contributors_router.register('users',
                             views.ContributorViewSet,
                             'contributors')

urlpatterns = [
    path('', include(projects_router.urls)),
    path('', include(contributors_router.urls))
]
