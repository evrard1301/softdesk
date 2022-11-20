from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


class SignupView(APIView):
    def post(self, request):
        try:
            data = request.data
            user = User.objects.create_user(
                username=data.get('username'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                password=data.get('password')
            )
            user.full_clean()
            user.save()
            data = UserSerializer(user).data
            return Response(data)

        except Exception:
            return Response({'status': 'err'}, status=401)
