from django.contrib.auth import get_user_model
from .models import Trip, TripState, TripEvent
from django.test import TestCase


class UsersManagersTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.superuser = self.User.objects.create_superuser(email='super@user.com', name='test', date_of_birth='2002-12-12', password='hello_world')
        self.normaluser = self.User.objects.create_user(email='normal@user.com', name='test1', date_of_birth='2002-12-12', password='hello_world')

    def test_create_trip(self):
        trip = Trip.objects.create(user=self.normaluser)

        with self.assertRaises(Exception):
            TripState.objects.create(trip=trip, current_rate='night')
        with self.assertRaises(Exception):
            TripState.objects.create(trip=trip, current_rate='day', fare=-5)
        with self.assertRaises(Exception):
            TripState.objects.create(trip=trip, current_rate='day', parking_price=-2)
        with self.assertRaises(Exception):
            TripState.objects.create(trip=trip, current_rate='evening', reservation_price=-3)

        with self.assertRaises(Exception):
            TripEvent.objects.create(trip=trip, event='flying')
        with self.assertRaises(Exception):
            TripEvent.objects.create(trip=trip, event='start', cost=-50)
