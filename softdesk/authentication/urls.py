from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('signup/', views.LoginView.as_view(), name='signup')
]
