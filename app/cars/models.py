from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    day_fare = models.FloatField()
    evening_fare = models.FloatField()
    parking_price = models.FloatField()
    reservation_price = models.FloatField()


class Car(models.Model):
    brand = models.CharField(max_length=50)
    register_number = models.CharField(max_length=8)
    color = models.CharField(max_length=30)
    year = models.IntegerField()
    weight = models.IntegerField()
    mileage = models.IntegerField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class CarInfo(models.Model):
    car_id = models.OneToOneField(Car, on_delete=models.CASCADE, primary_key=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    petrol_level = models.IntegerField()
    status = models.CharField(max_length=50)
