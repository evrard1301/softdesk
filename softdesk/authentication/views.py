from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . import models


class LoginView(APIView):
    def post(self, request):
        id = None
        
        try:
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            
            user = models.User.objects.create_user(username=username,
                                                   password=password)
            id = user.id
            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            user.full_clean()
            user.save()
        except Exception as err:
            if id is not None:
                models.User.objects.filter(id=id)[0].delete()
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(err))
        
        return Response(status=status.HTTP_201_CREATED)
