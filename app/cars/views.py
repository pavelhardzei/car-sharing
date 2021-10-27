from rest_framework import permissions, viewsets, generics, status
from rest_framework.response import Response
from .models import Category, Car, CarInfo
from .serializers import CategorySerializer, CarSerializer, CarInfoSerializer
import cars.utils as utils
from base_app.mixins import QueryParamsMixin


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


class AvailableCars(generics.ListAPIView, QueryParamsMixin):
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Car.objects.select_related('car_info').filter(car_info__status=CarInfo.Status.available)

    def list(self, request, *args, **kwargs):
        params = self.query_params(request, ('longitude', 'latitude', 'radius'))

        available_cars = self.get_queryset()
        if available_cars.count() == 0:
            return Response({'message': 'No available cars'}, status=status.HTTP_404_NOT_FOUND)

        loc = params['longitude'], params['latitude']
        distances = utils.count_distances(loc, available_cars)

        cars_ser = CarSerializer(available_cars, many=True)
        for car, dist in zip(cars_ser.data, distances):
            car.update({'dist_to': dist})

        filtered = utils.filter_distances(cars_ser.data, params['radius'])
        if not filtered:
            return Response({'message': 'No available cars in given radius'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'your_location': loc, 'available_cars': filtered})
