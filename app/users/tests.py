from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status, permissions
from .permissions import IsAdminOrOwner


class UsersManagersTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.superuser = self.User.objects.create_superuser(email='super@user.com', name='test', date_of_birth='2002-12-12', password='hello_world')
        self.normaluser = self.User.objects.create_user(email='normal@user.com', name='test1', date_of_birth='2002-12-12', password='hello_world')

        self.factory = RequestFactory()

        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.normaluser)

    def test_permissions(self):
        permission = permissions.IsAdminUser()

        request = self.factory.get(reverse('users'))
        request.user = self.superuser
        self.assertTrue(permission.has_permission(request, None))
        request.user = self.normaluser
        self.assertFalse(permission.has_permission(request, None))

        permission = IsAdminOrOwner()
        request = self.factory.get(reverse('user_detail', kwargs={'pk': self.superuser.pk}))
        request.user = self.normaluser
        self.assertFalse(permission.has_object_permission(request, None, self.superuser))

        request = self.factory.get(reverse('user_detail', kwargs={'pk': self.normaluser.pk}))
        request.user = self.superuser
        self.assertTrue(permission.has_object_permission(request, None, self.normaluser))


    def test_signup(self):
        response = self.client.post(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('users'), {'email': 'new@user.com', 'name': 'new_user', 'date_of_birth': '2000-01-01', 'password': 'hello_world'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        response = self.api_client.put(reverse('update_user', kwargs={'pk': self.normaluser.pk}), {'email': 'changed@user.com', 'name': 'changed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = self.User.objects.get(pk=self.normaluser.pk)
        self.assertEqual(user.email, 'changed@user.com')
        self.assertEqual(user.name, 'changed')

    def test_change_password(self):
        response = self.api_client.put(reverse('change_password', kwargs={'pk': 'me'}), {'old_password': 'hello_world',
                                       'password': 'testing321', 'password_rep': 'testing321'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.User.objects.get(pk=self.normaluser.pk).check_password('testing321'))

    def test_delete(self):
        response = self.api_client.delete(reverse('user_detail', kwargs={'pk': 'me'}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
