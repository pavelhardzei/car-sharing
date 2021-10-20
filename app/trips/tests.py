from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Trip, TripState, TripEvent
from cars.models import Car, Category, CarInfo
from django.test import TestCase
from unittest.mock import patch


@patch('rest_framework.views.APIView.check_permissions', lambda *args, **kwargs: True)
class TripsTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.superuser = self.User.objects.create_superuser(email='super@user.com', name='test', date_of_birth='2002-12-12', password='hello_world')
        self.normaluser = self.User.objects.create_user(email='normal@user.com', name='test1', date_of_birth='2002-12-12', password='hello_world')

        self.test_category = Category.objects.create(name='Economy', day_fare=6, evening_fare=8, parking_price=2, reservation_price=3)
        self.test_car = Car.objects.create(brand='BMW', register_number='1111KK-1', color=Car.Color.blue, year=2020, weight=600, mileage=1000, category=self.test_category)
        self.test_car_info = CarInfo.objects.create(car=self.test_car, longitude='33.123456', latitude='34.451222', petrol_level=100, status=CarInfo.Status.available)

        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.normaluser)

    def test_create_trip(self):
        response = self.api_client.post(reverse('management'), {'car_id': self.test_car.id, 'action': TripEvent.Event.landing})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_trip_with_booking(self):
        response = self.api_client.post(reverse('management'), {'car_id': self.test_car.id, 'action': TripEvent.Event.booking})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.api_client.post(reverse('management'), {'car_id': self.test_car.id, 'action': TripEvent.Event.landing})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_make_invalid_requests_when_booking(self):
        self.api_client.post(reverse('management'), {'car_id': self.test_car.id, 'action': TripEvent.Event.booking})
        response = self.api_client.post(reverse('management'), {'car_id': self.test_car.id, 'action': TripEvent.Event.booking})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_make_invalid_requests_when_landing(self):
        self.api_client.post(reverse('management'), {'car_id': self.test_car.id, 'action': TripEvent.Event.booking})
        self.api_client.post(reverse('management'), {'car_id': self.test_car.id, 'action': TripEvent.Event.landing})
        response = self.api_client.post(reverse('management'), {'car_id': self.test_car.id, 'action': TripEvent.Event.landing})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_trip_maintenance(self):
        self.api_client.post(reverse('management'), {'car_id': self.test_car.id, 'action': TripEvent.Event.landing})
        trip = Trip.objects.all().first()
        response = self.api_client.post(reverse('maintenance'), {'car': self.test_car.id, 'event': TripEvent.Event.washing,
                                        'credentials': 'some creds', 'petrol_level': 50, 'longitude': '33.123453',
                                        'latitude': '31.674566', 'total_distance': 20})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
