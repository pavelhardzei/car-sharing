from rest_framework import permissions, viewsets, views, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Trip, TripState, TripEvent
from cars.models import Car, CarInfo
from cars.serializers import CarSerializer
from .serializers import TripSerializer, TripStateSerializer, TripEventSerializer
import datetime


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


class TripManagement(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_car(self, pk):
        return Car.objects.select_related('car_info').get(pk=pk)

    def get_current_trip(self, user_id):
        try:
            return Trip.objects.select_related('state').prefetch_related('events').get(user=user_id, end_date=None)
        except Trip.DoesNotExist:
            return None

    def create_trip(self, user, car):
        current_trip = self.get_current_trip(user.id)
        if current_trip is not None:
            raise ValidationError({'error_message': 'Your trip already exists'})
        if car.car_info.status != CarInfo.Status.available:
            raise ValidationError({'error_message': f'Car is {car.car_info.status}, choose another one'})

        trip = Trip.objects.create(car=car, user=user)
        if 4 <= datetime.datetime.now().hour < 18:
            rate = TripState.Rate.day
            fare = car.category.day_fare
        else:
            rate = TripState.Rate.evening
            fare = car.category.evening_fare
        TripState.objects.create(trip=trip, current_rate=rate, fare=fare, parking_price=car.category.parking_price,
                                 reservation_price=car.category.reservation_price)

        car.car_info.status = CarInfo.Status.busy
        car.car_info.save()

        return trip

    def get(self, request):
        current_trip = self.get_current_trip(request.user.id)
        if current_trip is None:
            return Response({'message': 'You haven\'t got started trips'})

        trip_ser = TripSerializer(current_trip)
        return Response(trip_ser.data)

    def post(self, request):
        fields = ('car_id', 'action')
        for field in fields:
            if field not in request.data:
                raise ValidationError({'error_message': f'{field} is required'})
        car_id = request.data['car_id']
        action = request.data['action']
        car = self.get_car(car_id)

        if action == TripEvent.Event.booking:
            trip = self.create_trip(request.user, car)
            TripEvent.objects.create(trip=trip, event=TripEvent.Event.booking)
            trip_ser = TripSerializer(trip)

            return Response(trip_ser.data, status=status.HTTP_201_CREATED)
        elif action == TripEvent.Event.landing:
            current_trip = self.get_current_trip(request.user.id)
            if current_trip is not None:
                if current_trip.events.first().event != TripEvent.Event.booking or len(current_trip.events.all()) != 1:
                    raise ValidationError({'error_message': 'Your trip already exists'})

                event = TripEvent.objects.create(trip=current_trip, event=TripEvent.Event.landing)
                current_trip.events.add(event)
                trip_ser = TripSerializer(current_trip)

                return Response(trip_ser.data, status=status.HTTP_200_OK)
            else:
                trip = self.create_trip(request.user, car)
                TripEvent.objects.create(trip=trip, event=TripEvent.Event.landing)
                trip_ser = TripSerializer(trip)

                return Response(trip_ser.data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError({'error_message': 'Invalid action'})


class TripsHistory(generics.ListAPIView):
    serializer_class = TripSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Trip.objects.select_related('state').prefetch_related('events')\
            .filter(user=self.request.user.id).order_by('-id')
