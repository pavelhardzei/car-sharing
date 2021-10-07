from django.contrib.auth import get_user_model
from .models import Category, Car, CarInfo
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import permissions


class UsersManagersTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.superuser = self.User.objects.create_superuser(email='super@user.com', name='test', date_of_birth='2002-12-12', password='hello_world')
        self.normaluser = self.User.objects.create_user(email='normal@user.com', name='test1', date_of_birth='2002-12-12', password='hello_world')

        self.factory = RequestFactory()

    def test_create_car(self):
        with self.assertRaises(Exception):
            Category.objects.create(name='Economy', day_fare=-1, evening_fare=8, parking_price=2, reservation_price=3)
        with self.assertRaises(Exception):
            Category.objects.create(name='Economy', day_fare=6, evening_fare=8, parking_price=-2, reservation_price=3)
        with self.assertRaises(Exception):
            Category.objects.create(name='Economy', day_fare=-1, evening_fare=8, parking_price=2, reservation_price=0)

        cat1 = Category.objects.create(name='Economy', day_fare=6, evening_fare=8, parking_price=2, reservation_price=3)

        with self.assertRaises(Exception):
            Car.objects.create(brand='Mercedes', register_number='1111KK-1', color='purple', year=2020, weight=600, mileage=1000, category=cat1)
        with self.assertRaises(Exception):
            Car.objects.create(brand='Mercedes', register_number='1111KK-1', color=Car.Color.blue, year=3020, weight=600, mileage=1000, category=cat1)
        with self.assertRaises(Exception):
            Car.objects.create(brand='Mercedes', register_number='1111KK-1', color=Car.Color.blue, year=2020, weight=-600, mileage=1000, category=cat1)
        with self.assertRaises(Exception):
            Car.objects.create(brand='Mercedes', register_number='1111KK-1', color=Car.Color.blue, year=2020, weight=600, mileage=-1000, category=cat1)

        car1 = Car.objects.create(brand='Mercedes', register_number='1111KK-1', color=Car.Color.blue, year=2020, weight=600, mileage=1000, category=cat1)

        with self.assertRaises(Exception):
            CarInfo.objects.create(car=car1, longitude='290.345612', latitude='34.124533', petrol_level=90, status=CarInfo.Status.available)
        with self.assertRaises(Exception):
            CarInfo.objects.create(car=car1, longitude='20.345612', latitude='95.124533', petrol_level=90, status=CarInfo.Status.available)
        with self.assertRaises(Exception):
            CarInfo.objects.create(car=car1, longitude='20.345612', latitude='34.124533', petrol_level=-90, status=CarInfo.Status.available)
        with self.assertRaises(Exception):
            CarInfo.objects.create(car=car1, longitude='20.345612', latitude='34.124533', petrol_level=90, status='free')

        CarInfo.objects.create(car=car1, longitude='33.345612', latitude='34.124533', petrol_level=90, status=CarInfo.Status.available)

        with self.assertRaises(Exception):
            CarInfo.objects.create(car=car1, longitude='33.345612', latitude='34.124533', petrol_level=90, status=CarInfo.Status.available)

    def test_permission(self):
        self.permission = permissions.IsAdminUser()

        request = self.factory.get(reverse('car-list'))
        request.user = self.normaluser
        self.assertFalse(self.permission.has_permission(request, None))
        request.user = self.superuser
        self.assertTrue(self.permission.has_permission(request, None))
