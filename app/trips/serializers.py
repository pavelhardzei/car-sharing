from rest_framework import serializers
from .models import Trip, TripState, TripEvent


class TripStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripState
        fields = ('trip', 'current_rate', 'fare', 'parking_price', 'reservation_price')

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
        fields = ('id', 'trip', 'event', 'timestamp', 'credentials', 'cost')

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
        fields = ('id', 'state', 'car', 'user', 'total_cost', 'start_date', 'end_date', 'total_distance',
                  'reservation_time', 'events')

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
        start_date = data.get('start_date', self.instance.start_date)
        end_date = data.get('end_date', None)
        if end_date and end_date <= start_date:
            raise Exception('End date must occur after start date')
        return data
