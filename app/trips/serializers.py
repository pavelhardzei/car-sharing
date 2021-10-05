from rest_framework import serializers
from .models import Trip, TripState, TripEvent


class TripStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripState
        fields = '__all__'


class TripEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripEvent
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    state = TripStateSerializer(read_only=True)
    events = TripEventSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'
