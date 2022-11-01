from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User


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
            return Response({'status': 'ok'})

        except Exception as e:
            return Response({'status': 'err'})
