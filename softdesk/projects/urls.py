from django.urls import path, include
from rest_framework_nested import routers
from . import views

app_name = 'projects'

router = routers.SimpleRouter()
router.register('projects', views.ProjectView, basename='projects')

urlpatterns = [
    path('/', include(router.urls))
]
