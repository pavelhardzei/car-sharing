from rest_framework import serializers
from .models import Category, Car, CarInfo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'day_fare', 'evening_fare', 'parking_price', 'reservation_price')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'brand', 'register_number', 'color', 'year', 'weight', 'mileage', 'category_id')


class CarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarInfo
        fields = ('car_id', 'longitude', 'latitude', 'petrol_level', 'status')
