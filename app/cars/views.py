from rest_framework import viewsets
from rest_framework import permissions
from .models import Category, Car, CarInfo
from .serializers import CategorySerializer, CarSerializer, CarInfoSerializer


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
