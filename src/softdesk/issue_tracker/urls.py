from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'issue_tracker'

router = routers.DefaultRouter()
router.register('projects', views.ProjectViewSet, basename='projects')

urlpatterns = [
    path('projects/<int:id>/users/',
         views.ContributorAPIView.as_view({
             'post': 'create',
             'get': 'list',
             'delete': 'delete'
         }),
         name='contributor'),
    path('', include(router.urls))
]
