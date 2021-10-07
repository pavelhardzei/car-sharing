from rest_framework import permissions
from rest_framework import viewsets
from .models import Trip, TripState, TripEvent
from .serializers import TripSerializer, TripStateSerializer, TripEventSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related('state').prefetch_related('events').all()
    serializer_class = TripSerializer
    permission_classes = (permissions.IsAdminUser, )


class TripStateViewSet(viewsets.ModelViewSet):
    queryset = TripState.objects.all()
    serializer_class = TripStateSerializer
    permission_classes = (permissions.IsAdminUser, )


class TripEventViewSet(viewsets.ModelViewSet):
    queryset = TripEvent.objects.all()
    serializer_class = TripEventSerializer
    permission_classes = (permissions.IsAdminUser, )
