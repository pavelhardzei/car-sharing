from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse
import json
from rest_framework.test import APIClient
from rest_framework import status


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', name='test', date_of_birth='2002-12-12')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.name, 'test')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='normal@user.com', name='test', date_of_birth='2002-12-12')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', name='', date_of_birth='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='normal2@user.com', name='test', date_of_birth='2012-12-12')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', name='test', date_of_birth='2000-12-12')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='super2@user.com', name='test2', date_of_birth='2000-12-12',
                                          is_superuser=False)

    def test_permissions(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        User = get_user_model()
        superuser = User.objects.create_superuser(email='super@user.com', name='test', date_of_birth='2002-12-12', password='hello_world')
        user = User.objects.create_user(email='normal@user.com', name='test1', date_of_birth='2002-12-12', password='hello_world')
        superuser.save()
        user.save()

        response = self.client.post(reverse('get_token'), {'email_or_username': 'test', 'password': 'hello_world'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = json.loads(response.content)['token']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(reverse('user_detail', kwargs={'pk': superuser.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.get(reverse('user_detail', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(reverse('get_token'), {'email_or_username': 'normal@user.com', 'password': 'hello_world'})
        token = json.loads(response.content)['token']
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.get(reverse('user_detail', kwargs={'pk': superuser.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = client.get(reverse('user_detail', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup(self):
        response = self.client.post(reverse('signup'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('signup'), {'email': 'normal@user.com', 'name': 'test',
                                                        'date_of_birth': '2000-01-01', 'password': 'hello_world'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
