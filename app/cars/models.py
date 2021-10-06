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

    def clean(self):
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
    car = models.OneToOneField(Car, on_delete=models.CASCADE, primary_key=True, related_name='car_info')
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    petrol_level = models.IntegerField()
    status = models.CharField(max_length=50)

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
