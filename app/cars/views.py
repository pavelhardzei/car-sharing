from rest_framework import permissions, viewsets, views
from rest_framework.response import Response
from .models import Category, Car, CarInfo
from .serializers import CategorySerializer, CarSerializer, CarInfoSerializer
import math
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


class AvailableCars(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_user_location(self, user):
        # return user location
        longitude, latitude = Decimal('-1.72972222'), Decimal('53.32055555')  # example
        return longitude, latitude

    def get(self, request):
        available_cars = Car.objects.select_related('car_info').filter(car_info__status=CarInfo.Status.available)
        if available_cars.count() == 0:
            return Response({'message': 'No available cars'})

        loc = self.get_user_location(request.user)
        loc_rad = loc[0] * Decimal(math.pi) / 180, loc[1] * Decimal(math.pi) / 180
        cars_locs_rad = [(car.car_info.longitude * Decimal(math.pi) / 180,
                          car.car_info.latitude * Decimal(math.pi) / 180) for car in available_cars]

        earth_radius = 6378.8
        distances = [earth_radius * math.acos(math.sin(loc_rad[1]) * math.sin(car_loc[1]) +
                     math.cos(loc_rad[1]) * math.cos(car_loc[1]) * math.cos(car_loc[0] - loc_rad[0]))
                     for car_loc in cars_locs_rad]

        cars_ser = CarSerializer(available_cars, many=True)
        cars_dist = [(car, {'dist_to': dist}) for car, dist in zip(cars_ser.data, distances)]

        return Response({'your_location': loc, 'available_cars': cars_dist})
