from rest_framework import permissions, viewsets, views, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
from .models import Trip, TripState, TripEvent
from cars.models import Car, CarInfo
from cars.serializers import CarSerializer, CarInfoSerializer
from .serializers import TripSerializer, TripStateSerializer, TripEventSerializer, TripSerializerHistory
from base_app.exceptions import LogicError
import datetime
import random


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related('state', 'car', 'car__car_info').prefetch_related('events').all()
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


class TripManagement(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_current_trip(self, user_id):
        try:
            return Trip.objects.select_related('state', 'car', 'car__car_info').prefetch_related('events').get(end_date=None, user=user_id)
        except Trip.DoesNotExist:
            return None

    def get_car(self, pk):
        try:
            return Car.objects.select_related('car_info').get(pk=pk)
        except Car.DoesNotExist:
            raise ValidationError({'error_message': 'car doesn\'t exist'})

    def get_rate(self, car):
        if 4 <= datetime.datetime.now().hour < 18:
            rate = TripState.Rate.day
            fare = car.category.day_fare
        else:
            rate = TripState.Rate.evening
            fare = car.category.evening_fare

        return rate, fare

    def create_trip(self, user, car, event):
        current_trip = self.get_current_trip(user.id)
        if current_trip:
            raise LogicError('Your trip already exists', status_code=status.HTTP_400_BAD_REQUEST)
        if car.car_info.status != CarInfo.Status.available:
            raise LogicError(f'Car is {car.car_info.status}, choose another one', status_code=status.HTTP_400_BAD_REQUEST)

        trip = Trip.objects.create(car=car, user=user)
        rate, fare = self.get_rate(car)
        TripState.objects.create(trip=trip, current_rate=rate, fare=fare, parking_price=car.category.parking_price,
                                 reservation_price=car.category.reservation_price)
        TripEvent.objects.create(trip=trip, event=event)

        car.car_info.status = CarInfo.Status.busy
        car.car_info.save()

        return trip

    def get(self, request):
        current_trip = self.get_current_trip(request.user.id)
        if current_trip is None:
            return Response({'message': 'You haven\'t got started trips'})

        trip_ser = TripSerializer(current_trip)
        return Response(trip_ser.data)

    @transaction.atomic
    def post(self, request):
        fields = ('car_id', 'action')
        for field in fields:
            if field not in request.data:
                raise ValidationError({'error_message': f'{field} is required'})
        action = request.data['action']

        if action not in (TripEvent.Event.booking, TripEvent.Event.landing):
            raise ValidationError({'error_message': 'Invalid action'})

        current_trip = self.get_current_trip(request.user.id)
        if current_trip is None:
            trip = self.create_trip(request.user, self.get_car(request.data['car_id']), action)
            trip_ser = TripSerializer(trip)
            return Response(trip_ser.data, status=status.HTTP_201_CREATED)

        if action == TripEvent.Event.booking or current_trip.events.first().event != TripEvent.Event.booking or current_trip.events.count() != 1:
            raise LogicError('Your trip already exists', status_code=status.HTTP_400_BAD_REQUEST)

        event = TripEvent.objects.create(trip=current_trip, event=TripEvent.Event.landing)
        current_trip.events.add(event)
        current_trip.reservation_time = (event.timestamp - current_trip.events.first().timestamp).total_seconds() // 60
        current_trip.save()
        trip_ser = TripSerializer(current_trip)

        return Response(trip_ser.data)


class TripMaintenance(views.APIView):
    permission_classes = (permissions.IsAdminUser, )

    def get_current_trip(self, car_id):
        try:
            return Trip.objects.select_related('state', 'car', 'car__car_info').prefetch_related('events').get(end_date=None, car=car_id)
        except Trip.DoesNotExist:
            return None

    def pay_by_credentials(self, credentials):
        # Some bank operations
        cost = random.randint(1, 5)
        return cost

    @transaction.atomic
    def post(self, request):
        fields = ('car', 'event', 'credentials', 'petrol_level', 'longitude', 'latitude', 'total_distance')
        for field in fields:
            if field not in request.data:
                raise ValidationError({'error_message': f'{field} is required'})

        trip = self.get_current_trip(request.data['car'])
        if trip is None:
            return Response({'message': 'Current trip doesn\'t exist'})

        car = trip.car
        event = request.data['event']
        credentials = request.data['credentials']

        filtered = {k: v for k, v in request.data.items() if v}

        car_info_ser = CarInfoSerializer(car.car_info, data=filtered, partial=True)
        car_info_ser.is_valid(raise_exception=True)
        car_info_ser.save()

        trip_ser = TripSerializer(trip, data=filtered, partial=True)
        trip_ser.is_valid(raise_exception=True)
        trip_ser.save()

        if event is None:
            return Response(trip_ser.data)
        if event not in TripEvent.Event.values or event in (TripEvent.Event.booking, TripEvent.Event.landing, TripEvent.Event.end):
            raise ValidationError({'error_message': 'Invalid event'})

        trip_event = TripEvent(trip=trip, event=event)
        previous_event = trip.events.last()

        if event != TripEvent.Event.end_parking and previous_event.event == TripEvent.Event.parking:
            raise LogicError(f'Event \'{event}\' cannot occur after \'{previous_event.event}\'', status_code=status.HTTP_400_BAD_REQUEST)
        if event == TripEvent.Event.end_parking and previous_event.event != TripEvent.Event.parking:
            raise LogicError(f'Event \'{event}\' must occur after \'{TripEvent.Event.parking}\'', status_code=status.HTTP_400_BAD_REQUEST)
        if event in (TripEvent.Event.fueling, TripEvent.Event.washing) and credentials is None:
            raise LogicError(f'Credentials must be transferred when \'{event}\'', status_code=status.HTTP_400_BAD_REQUEST)

        if credentials:
            trip_event.credentials = credentials
            trip_event.cost = self.pay_by_credentials(credentials)
            trip.total_cost += trip_event.cost
            trip.save()

        trip_event.save()
        trip.events.add(trip_event)

        return Response(trip_ser.data)


class TripsHistory(generics.ListAPIView):
    serializer_class = TripSerializerHistory
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Trip.objects.select_related('state', 'car').prefetch_related('events')\
            .filter(user=self.request.user.id).order_by('-id')


class TripCost(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_current_trip(self, user_id):
        try:
            return Trip.objects.select_related('state', 'car', 'car__car_info').prefetch_related('events').get(end_date=None, user=user_id)
        except Trip.DoesNotExist:
            return None

    def get(self, request):
        trip = self.get_current_trip(request.user.id)
        if trip is None:
            return Response({'message': 'Current trip doesn\'t exist'})
        total_cost, _ = trip.get_total_cost()
        trip_ser = TripSerializer(trip)

        return Response({'total_cost': total_cost, 'trip': trip_ser.data})


class TripEnd(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_current_trip(self, user_id):
        try:
            return Trip.objects.select_related('state', 'car', 'car__car_info').prefetch_related('events').get(end_date=None, user=user_id)
        except Trip.DoesNotExist:
            return None

    def pay_for_trip(self, total_cost):
        # Pay for the trip using users bank card props?
        bank_check = 'some info'
        return bank_check

    @transaction.atomic
    def post(self, request):
        trip = self.get_current_trip(request.user.id)
        if trip is None:
            return Response({'message': 'Current trip doesn\'t exist'})
        total_cost, end_date = trip.get_total_cost()

        event = TripEvent.objects.create(trip=trip, event=TripEvent.Event.end, timestamp=end_date)
        trip.events.add(event)
        trip.total_cost = total_cost
        trip.end_date = end_date
        trip.save()

        trip.car.car_info.status = CarInfo.Status.available
        trip.car.car_info.save()

        bank_check = self.pay_for_trip(total_cost)

        trip_ser = TripSerializer(trip)
        return Response({'trip': trip_ser.data, 'check': bank_check})
