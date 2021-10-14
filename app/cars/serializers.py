from rest_framework import serializers
from .models import Category, Car, CarInfo
import datetime


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'day_fare', 'evening_fare', 'parking_price', 'reservation_price')

    def validate_day_fare(self, value):
        if value <= 0:
            raise Exception('Day fare must be positive')
        return value

    def validate_evening_fare(self, value):
        if value <= 0:
            raise Exception('Evening fare must be positive')
        return value

    def validate_reservation_price(self, value):
        if value <= 0:
            raise Exception('Reservation price must be positive')
        return value

    def validate_parking_price(self, value):
        if value < 0:
            raise Exception('Parking price cannot be negative')
        return value


class CarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarInfo
        fields = ('car', 'longitude', 'latitude', 'petrol_level', 'status')

        extra_kwargs = {
            'car': {
                'write_only': True
            }
        }

    def validate_petrol_level(self, value):
        if value < 0 or value > 100:
            raise Exception('Petrol level must be in range(0, 100)')
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise Exception('Longitude must be in range(-180, 180)')
        return value

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise Exception('Latitude must be in range(-90, 90)')
        return value


class CarSerializer(serializers.ModelSerializer):
    car_info = CarInfoSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ('id', 'car_info', 'brand', 'register_number', 'color', 'year', 'weight', 'mileage', 'category')

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and (request.method == 'PUT' or request.method == 'PATCH'):
            fields['year'].read_only = True
        return fields

    def validate_year(self, value):
        if value < 1886 or value > datetime.date.today().year:
            raise Exception('Invalid creation year')
        return value

    def validate_weight(self, value):
        if value <= 0:
            raise Exception('Weight must be positive')
        return value

    def validate_mileage(self, value):
        if value < 0:
            raise Exception('Mileage cannot be negative')
        return value
