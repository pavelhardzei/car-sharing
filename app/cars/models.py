from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    day_fare = models.FloatField()
    evening_fare = models.FloatField()
    parking_price = models.FloatField()
    reservation_price = models.FloatField()

    def __str__(self):
        return self.name


class Car(models.Model):
    brand = models.CharField(max_length=50)
    register_number = models.CharField(max_length=8, unique=True)
    color = models.CharField(max_length=30)
    year = models.IntegerField(editable=False)
    weight = models.IntegerField()
    mileage = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return self.register_number


class CarInfo(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, primary_key=True, related_name='car_info')
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    petrol_level = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return str(self.car)
