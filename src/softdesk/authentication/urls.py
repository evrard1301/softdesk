from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

app_name = 'authentication'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login')
]
