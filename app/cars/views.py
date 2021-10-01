from rest_framework import generics
from .models import Category, Car, CarInfo
from .serializers import CategorySerializer, CarSerializer, CarInfoSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CarList(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarInfoList(generics.ListCreateAPIView):
    queryset = CarInfo.objects.all()
    serializer_class = CarInfoSerializer
