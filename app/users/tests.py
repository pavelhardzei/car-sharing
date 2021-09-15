from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.utils import IntegrityError


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
            User.objects.create_superuser(email='super2@user.com', name='test', date_of_birth='2000-12-12',
                                          is_superuser=False)
