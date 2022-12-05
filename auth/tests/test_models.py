from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class TestModel(APITestCase):
    def test_creates_user(self):
        email = 'email@email.com'
        password = '123'
        username = ''
        user = User.objects.create_user(username, email, password)

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_creates_superuser(self):
        email = 'email@email.com'
        password = '123'
        username = ''
        user = User.objects.create_superuser(username, email, password)

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_raises_error_when_no_email(self):
        def create():
            email = ''
            password = '123'
            username = ''
            user = User.objects.create_superuser(username, email, password)

        self.assertRaises(ValueError, create)

        