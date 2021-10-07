from rest_framework import serializers
from .models import Category, Car, CarInfo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'day_fare', 'evening_fare', 'parking_price', 'reservation_price')


class CarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarInfo
        fields = ('car', 'longitude', 'latitude', 'petrol_level', 'status')

        extra_kwargs = {
            'car': {
                'write_only': True
            }
        }


class CarSerializer(serializers.ModelSerializer):
    car_info = CarInfoSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ('id', 'brand', 'register_number', 'color', 'year', 'weight', 'mileage', 'category', 'car_info')

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and (request.method == 'PUT' or request.method == 'PATCH'):
            fields['year'].read_only = True
        return fields
