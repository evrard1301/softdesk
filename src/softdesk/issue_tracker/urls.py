from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter
from . import views

app_name = 'issue_tracker'

############
# PROJECTS #
############

projects_router = routers.DefaultRouter()
projects_router.register('projects', views.ProjectViewSet, basename='projects')

################
# CONTRIBUTORS #
################

contributors_router = NestedSimpleRouter(projects_router,
                                         'projects',
                                         lookup='project')

contributors_router.register('users',
                             views.ContributorViewSet,
                             'contributors')
##########
# ISSUES #
##########

issues_router = NestedSimpleRouter(projects_router, 'projects', lookup='projects')
issues_router.register('issues', views.IssueViewSet, 'issues')

urlpatterns = [
    path('', include(projects_router.urls)),
    path('', include(contributors_router.urls)),
    path('', include(issues_router.urls))
]
