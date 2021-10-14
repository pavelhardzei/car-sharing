from django.contrib.auth import get_user_model
from .models import Trip, TripState, TripEvent
from django.test import TestCase


class TripsTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.superuser = self.User.objects.create_superuser(email='super@user.com', name='test', date_of_birth='2002-12-12', password='hello_world')
        self.normaluser = self.User.objects.create_user(email='normal@user.com', name='test1', date_of_birth='2002-12-12', password='hello_world')

    def test_create_trip(self):
        pass
