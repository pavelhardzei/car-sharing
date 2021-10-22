from rest_framework import permissions, viewsets, generics
from rest_framework.response import Response
from .models import Category, Car, CarInfo
from .serializers import CategorySerializer, CarSerializer, CarInfoSerializer
import cars.utils as utils
from decimal import Decimal


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUser, )


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.select_related('car_info').all()
    serializer_class = CarSerializer
    permission_classes = (permissions.IsAdminUser, )


class CarInfoViewSet(viewsets.ModelViewSet):
    queryset = CarInfo.objects.all()
    serializer_class = CarInfoSerializer
    permission_classes = (permissions.IsAdminUser, )


class AvailableCars(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_user_location(self, user):
        # return user location
        longitude, latitude = Decimal('-1.73972222'), Decimal('53.32055555')  # example
        return longitude, latitude

    def get_queryset(self):
        return Car.objects.select_related('car_info').filter(car_info__status=CarInfo.Status.available)

    def list(self, request, *args, **kwargs):
        available_cars = self.get_queryset()
        if available_cars.count() == 0:
            return Response({'message': 'No available cars'})

        loc = self.get_user_location(request.user)
        distances = utils.count_distances(loc, available_cars)

        cars_ser = CarSerializer(available_cars, many=True)
        cars_dist = [(car, {'dist_to': dist}) for car, dist in zip(cars_ser.data, distances)]

        return Response({'your_location': loc, 'available_cars': cars_dist})
