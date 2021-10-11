from rest_framework import serializers
from .models import Trip, TripState, TripEvent


class TripStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripState
        fields = '__all__'

        extra_kwargs = {
            'trip': {
                'write_only': True
            }
        }

    def validate_fare(self, value):
        if value and value <= 0:
            raise Exception('Fare must be positive')
        return value

    def validate_parking_price(self, value):
        if value and value < 0:
            raise Exception('Parking price cannot be negative')
        return value

    def validate_reservation_price(self, value):
        if value and value <= 0:
            raise Exception('Reservation price must be positive')
        return value


class TripEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripEvent
        fields = '__all__'

        extra_kwargs = {
            'trip': {
                'write_only': True
            }
        }

    def validate_cost(self, value):
        if value and value <= 0:
            raise Exception('Cost must be positive')
        return value


class TripSerializer(serializers.ModelSerializer):
    state = TripStateSerializer(read_only=True)
    events = TripEventSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'

    def validate_total_cost(self, value):
        if value and value <= 0:
            raise Exception('Cost must be positive')
        return value

    def validate_total_distance(self, value):
        if value and value < 0:
            raise Exception('Distance cannot be negative')
        return value

    def validate_reservation_time(self, value):
        if value and value <= 0:
            raise Exception('Reservation time must be positive')
        return value

    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['end_date'] and data['end_date'] <= data['start_date']:
                raise Exception('End date must occur after start date')
        return data
