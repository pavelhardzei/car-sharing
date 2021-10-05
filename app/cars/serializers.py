from rest_framework import serializers
from .models import Category, Car, CarInfo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarInfo
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    car = CarInfoSerializer(read_only=True)

    class Meta:
        model = Car
        fields = '__all__'
