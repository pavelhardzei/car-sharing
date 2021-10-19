from django.contrib.auth import get_user_model
from .models import Car, Category
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import permissions, status
import json
from unittest.mock import patch


@patch('rest_framework.views.APIView.check_permissions', lambda *args, **kwargs: True)
class CarsTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.superuser = self.User.objects.create_superuser(email='super@user.com', name='test', date_of_birth='2002-12-12', password='hello_world')
        self.normaluser = self.User.objects.create_user(email='normal@user.com', name='test1', date_of_birth='2002-12-12', password='hello_world')

        self.test_category = Category.objects.create(name='Economy', day_fare=6, evening_fare=8, parking_price=2, reservation_price=3)
        self.test_car = Car.objects.create(brand='BMW', register_number='1111KK-1', color=Car.Color.blue,
                                           year=2020, weight=600, mileage=1000, category=self.test_category)

        self.factory = RequestFactory()

    def test_create_car(self):
        response = self.client.post(reverse('category-list'), {'name': 'Comfort', 'day_fare': 10,
                                    'evening_fare': 15, 'parking_price': 2, 'reservation_price': 3})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('cars-list'), {'brand': 'KIA', 'register_number': '4400KC-4',
                                    'color': 'brawn', 'year': 2018, 'weight': 900, 'mileage': 2000, 'category': self.test_category.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('carinfo-list'), {'car': self.test_car.id, 'longitude': '30.234566',
                                        'latitude': '33.223456', 'petrol_level': 50, 'status': 'broken'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_car_with_invalid_fields(self):
        response = self.client.post(reverse('category-list'), {'name': 'Comfort', 'day_fare': 0,
                                        'evening_fare': 15, 'parking_price': 2, 'reservation_price': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('category-list'), {'name': 'Comfort', 'day_fare': 3,
                                        'evening_fare': 15, 'parking_price': -2, 'reservation_price': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('cars-list'), {'brand': 'KIA', 'register_number': '4400KC-4',
                                        'color': 'brawn', 'year': 2018, 'weight': 900, 'mileage': 2000, 'category': 100})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('cars-list'), {'brand': 'KIA', 'register_number': '4400KC-4',
                                        'color': 'brawn', 'year': 2300, 'weight': 900, 'mileage': 2000, 'category': self.test_category.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('carinfo-list'), {'car': 100, 'longitude': '30.234566',
                                        'latitude': '33.223456', 'petrol_level': 50, 'status': 'broken'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('carinfo-list'), {'car': self.test_car.id, 'longitude': '30.234566',
                                        'latitude': '33.223456', 'petrol_level': 50, 'status': 'running'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_year(self):
        year_change_to = 2000
        current_year = self.test_car.year
        response = self.client.patch(reverse('cars-detail', kwargs={'pk': self.test_car.id}), {'year': year_change_to},
                                     content_type='application/json')
        self.assertNotEqual(json.loads(response.content)['year'], year_change_to)
        self.assertEqual(json.loads(response.content)['year'], current_year)

    def test_delete_car(self):
        response = self.client.delete(reverse('cars-detail', kwargs={'pk': self.test_car.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Car.objects.all()), 0)

    def test_permission(self):
        self.permission = permissions.IsAdminUser()

        request = self.factory.get(reverse('cars-list'))
        request.user = self.normaluser
        self.assertFalse(self.permission.has_permission(request, None))
        request.user = self.superuser
        self.assertTrue(self.permission.has_permission(request, None))
