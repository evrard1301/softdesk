from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from .models import User


class SignUpTest(TestCase):
    def test_ok_signup(self):
        client = APIClient()

        response = client.post(reverse_lazy('authentication:signup'), {
            'username': 'alice00',
            'first_name': 'Alice',
            'last_name': 'Ecila',
            'password': 'alice-password',
            'email': 'alice@email.com'
        })

        self.assertEqual(200, response.status_code)

    def test_err_missing_username(self):
        client = APIClient()

        response = client.post(reverse_lazy('authentication:signup'), {
            'first_name': 'Alice',
            'last_name': 'Ecila',
            'password': 'alice-password',
            'email': 'alice@email.com'
        })

        self.assertNotEqual(200, response.status_code)

    def test_err_username_already_exists(self):
        client = APIClient()

        User.objects.create_user(username='alice00',
                                 password='alicia-password',
                                 email='alicia@email.com')

        response = client.post(reverse_lazy('authentication:signup'), {
            'username': 'alice00',
            'first_name': 'Alicia',
            'last_name': 'Aicila',
            'password': 'alicia-password',
            'email': 'alicia@email.com'
        })

        self.assertNotEqual(200, response.status_code)


class LoginTest(TestCase):
    def test_ok_login(self):
        client = APIClient()
        User.objects.create_user(username='alice', password='alice-password')

        response = client.post(reverse_lazy('authentication:login'), {
            'username': 'alice',
            'password': 'alice-password'
        })

        self.assertEqual(200, response.status_code)

    def test_err_wrong_credentials(self):
        client = APIClient()
        User.objects.create_user(username='alice', password='alice-password')

        response = client.post(reverse_lazy('authentication:login'), {
            'username': 'alicia',
            'password': 'alice-password'
        })

        self.assertEqual(401, response.status_code)
