from django.contrib.auth import get_user_model
from .models import Category, Car, CarInfo
from django.test import TestCase
from django.urls import reverse
import json
from rest_framework.test import APIClient
from rest_framework import status


class UsersManagersTests(TestCase):

    def test_create_car(self):
        category1 = Category.objects.create(name='Economy', day_fare=6, evening_fare=8, parking_price=2,
                                            reservation_price=3)
        category2 = Category.objects.create(name='Comfort', day_fare=7, evening_fare=9, parking_price=2,
                                            reservation_price=3)
        self.assertEqual(category1.id, 1)
        self.assertEqual(category1.name, 'Economy')
        car1 = Car.objects.create(brand='Mercedes', register_number='1111KK-1', color='dark blue', year=2020,
                                  weight=600, mileage=1000, category=category1)
        car2 = Car.objects.create(brand='BMW', register_number='2222KK-2', color='black', year=2021, weight=700,
                                  mileage=3000, category=category2)
        self.assertEqual(car1.category.id, 1)
        self.assertEqual(car2.category.id, 2)
        car_info1 = CarInfo.objects.create(car=car1, longitude='33.345612', latitude='34.124533', petrol_level=90,
                                           status='FREE')
        car_info2 = CarInfo.objects.create(car=car2, longitude='35.453312', latitude='36.442213', petrol_level=80,
                                           status='FREE')
        self.assertEqual(car_info1.car.register_number, '1111KK-1')
        self.assertEqual(car_info2.car.register_number, '2222KK-2')

        with self.assertRaises(Exception):
            CarInfo.objects.create(car=car1, longitude='33.345612', latitude='34.124533', petrol_level=90,
                                   status='FREE')

    def test_permissions(self):
        client = APIClient()
        User = get_user_model()
        User.objects.create_superuser(email='super@user.com', name='test', date_of_birth='2002-12-12',
                                                  password='hello_world')
        User.objects.create_user(email='normal@user.com', name='test1', date_of_birth='2002-12-12',
                                        password='hello_world')

        response = self.client.post(reverse('get_token'), {'name': 'test1', 'password': 'hello_world'})
        token = json.loads(response.content)['token']
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(reverse('get_token'), {'name': 'test', 'password': 'hello_world'})
        token = json.loads(response.content)['token']
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = client.post(reverse('category-list'),
                               {'name': 'Economy', 'day_fare': 6, 'evening_fare': 8, 'parking_price': 2,
                                'reservation_price': 3})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        category = Category.objects.all().get(name='Economy')
        response = client.post(reverse('car-list'),
                               {'brand': 'Mercedes', 'register_number': '7777KC-7', 'color': 'brawn', 'year': 2020,
                                'weight': 800, 'mileage': 1500, 'category': category.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        car = Car.objects.all().get(register_number='7777KC-7')
        response = client.post(reverse('car-list'),
                               {'brand': 'Mercedes', 'register_number': '7777KC-7', 'color': 'brawn', 'year': 2020,
                                'weight': 800, 'mileage': 1500, 'category': 100})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(reverse('carinfo-list'),
                               {'car': car.id, 'longitude': '33.345612', 'latitude': '34.124533', 'petrol_level': 90,
                                'status': 'FREE'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post(reverse('carinfo-list'),
                               {'car': car.id, 'longitude': '33.345612', 'latitude': '34.124533', 'petrol_level': 90,
                                'status': 'FREE'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
