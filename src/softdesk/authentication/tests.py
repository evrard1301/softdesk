from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class SignUpTest(TestCase):
    def test_ok_signup(self):
        client = APIClient()

        response = client.post(reverse_lazy('signup'), {
            'username': 'alice00',
            'first_name': 'Alice',
            'last_name': 'Ecila',
            'password': 'alice-password',
            'email': 'alice@email.com'
        })

        self.assertEqual('ok', response.data['status'])

    def test_err_missing_username(self):
        client = APIClient()

        response = client.post(reverse_lazy('signup'), {
            'first_name': 'Alice',
            'last_name': 'Ecila',
            'password': 'alice-password',
            'email': 'alice@email.com'
        })

        self.assertEqual('err', response.data['status'])

    def test_err_username_already_exists(self):
        client = APIClient()

        User.objects.create_user(username='alice00',
                                 password='alicia-password',
                                 email='alicia@email.com')

        response = client.post(reverse_lazy('signup'), {
            'username': 'alice00',
            'first_name': 'Alicia',
            'last_name': 'Aicila',
            'password': 'alicia-password',
            'email': 'alicia@email.com'
        })

        self.assertEqual('err', response.data['status'])
