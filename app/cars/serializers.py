from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Car, CarInfo
import datetime


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'day_fare', 'evening_fare', 'parking_price', 'reservation_price')

    def validate_day_fare(self, value):
        if value <= 0:
            raise ValidationError({'error_message': 'Day fare must be positive'})
        return value

    def validate_evening_fare(self, value):
        if value <= 0:
            raise ValidationError({'error_message': 'Evening fare must be positive'})
        return value

    def validate_reservation_price(self, value):
        if value <= 0:
            raise ValidationError({'error_message': 'Reservation price must be positive'})
        return value

    def validate_parking_price(self, value):
        if value < 0:
            raise ValidationError({'error_message': 'Parking price cannot be negative'})
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
            raise ValidationError({'error_message': 'Petrol level must be in range(0, 100)'})
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise ValidationError({'error_message': 'Longitude must be in range(-180, 180)'})
        return value

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise ValidationError({'error_message': 'Latitude must be in range(-90, 90)'})
        return value


class CarSerializerHistory(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'brand', 'register_number', 'color', 'year', 'weight', 'mileage', 'category')

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and (request.method == 'PUT' or request.method == 'PATCH'):
            fields['year'].read_only = True
        return fields

    def validate_year(self, value):
        if value < 1886 or value > datetime.date.today().year:
            raise ValidationError({'error_message': 'Invalid creation year'})
        return value

    def validate_weight(self, value):
        if value <= 0:
            raise ValidationError({'error_message': 'Weight must be positive'})
        return value

    def validate_mileage(self, value):
        if value < 0:
            raise ValidationError({'error_message': 'Mileage cannot be negative'})
        return value


class CarSerializer(CarSerializerHistory):
    car_info = CarInfoSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ('id', 'car_info', 'brand', 'register_number', 'color', 'year', 'weight', 'mileage', 'category')
