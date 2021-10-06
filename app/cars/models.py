from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    day_fare = models.FloatField()
    evening_fare = models.FloatField()
    parking_price = models.FloatField()
    reservation_price = models.FloatField()

    def clean(self):
        if self.day_fare <= 0 or self.evening_fare <= 0:
            raise Exception('Fare must be positive')
        if self.reservation_price <= 0:
            raise Exception('Reservation price must be positive')
        if self.parking_price < 0:
            raise Exception('Parking price cannot be negative')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Car(models.Model):
    class Color(models.TextChoices):
        red = ('red', 'RED')
        green = ('green', 'GREEN')
        blue = ('blue', 'BLUE')
        brawn = ('brawn', 'BRAWN')
        black = ('black', 'BLACK')
        gold = ('gold', 'GOLD')
        silver = ('silver', 'SILVER')

    brand = models.CharField(max_length=50)
    register_number = models.CharField(max_length=8, unique=True)
    color = models.CharField(max_length=30, choices=Color.choices)
    year = models.IntegerField()
    weight = models.IntegerField()
    mileage = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

    def clean(self):
        if self.year < 1886 or self.year > datetime.date.today().year:
            raise Exception('Invalid creation year')
        if self.weight <= 0:
            raise Exception('Weight must be positive')
        if self.mileage < 0:
            raise Exception('Mileage cannot be negative')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.register_number


class CarInfo(models.Model):
    class Status(models.TextChoices):
        available = ('available', 'AVAILABLE')
        broken = ('broken', 'BROKEN')
        busy = ('busy', 'BUSY')

    car = models.OneToOneField(Car, on_delete=models.CASCADE, primary_key=True, related_name='car_info')
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    petrol_level = models.IntegerField()
    status = models.CharField(max_length=50, choices=Status.choices)

    def clean(self):
        if self.petrol_level < 0 or self.petrol_level > 100:
            raise Exception('Petrol level must be in range(0, 100)')
        if self.longitude < -180 or self.longitude > 180:
            raise Exception('Longitude must be in range(-180, 180)')
        if self.latitude < -90 or self.latitude > 90:
            raise Exception('Latitude must be in range(-90, 90)')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.car)
