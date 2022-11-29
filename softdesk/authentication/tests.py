from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class CreateUserTest(TestCase):
    def test_ok_complete_user(self):
        client = APIClient()
        
        response = client.post(reverse_lazy('authentication:signup'), {
            'username': 'alice25',
            'first_name': 'Alice',
            'last_name': 'Morgan',
            'email': 'alice.morgan@email.com',
            'password': 'azerty'
        })

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        user = User.objects.all()[0]
        self.assertEqual('alice25', user.username)
        self.assertEqual('Alice', user.first_name)
        self.assertEqual('Morgan', user.last_name)
        self.assertEqual('alice.morgan@email.com', user.email)

    def test_err_incomplete_user(self):
        client = APIClient()
        
        response = client.post(reverse_lazy('authentication:signup'), {
            'username': 'alice25',
            'last_name': 'Morgan',
            'email': 'alice.morgan@email.com',
            'password': 'azerty'
        })

        self.assertNotEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(0, User.objects.count())

    def test_err_invalid_user(self):
        client = APIClient()
        
        response = client.post(reverse_lazy('authentication:signup'), {
            'username': 'alice25',
            'first_name': 'Alice',
            'last_name': 'Morgan',
            'email': 'notamail',
            'password': 'azerty'
        })

        self.assertNotEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(0, User.objects.count())

        
class LoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='alice',
                                             password='coucou')
        
    def test_ok(self):
        response = self.client.post(reverse_lazy('authentication:login'), {
            'username': 'alice',
            'password': 'coucou'
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(0, len(response.data))

    def test_err_wrong_username(self):
        response = self.client.post(reverse_lazy('authentication:login'), {
            'username': 'alicia',
            'password': 'coucou'
        })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_err_wrong_password(self):
        response = self.client.post(reverse_lazy('authentication:login'), {
            'username': 'alice',
            'password': 'salut'
        })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
