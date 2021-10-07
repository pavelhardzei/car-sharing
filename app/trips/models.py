from django.db import models
from django.utils import timezone
from users.models import UserAccount
from cars.models import Car


class Trip(models.Model):
    car = models.ForeignKey(Car, blank=True, null=True, default=None, on_delete=models.CASCADE, related_name='trips')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='trips')
    total_cost = models.FloatField(blank=True, null=True, default=None)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True, default=None)
    total_distance = models.IntegerField(blank=True, null=True, default=None)
    reservation_time = models.IntegerField(blank=True, null=True, default=None)

    def clean(self):
        if self.total_cost and self.total_cost <= 0:
            raise Exception('Cost must be positive')
        if self.end_date and self.end_date <= self.start_date:
            raise Exception('Invalid dates')
        if self.total_distance and self.total_distance <= 0:
            raise Exception('Distance must be positive')
        if self.reservation_time and self.reservation_time <= 0:
            raise Exception('Reservation time must be positive')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'id:{self.id}, car:{self.car}, user:{self.user}'


class TripState(models.Model):
    class Rate(models.TextChoices):
        day = ('day', 'DAY')
        evening = ('evening', 'EVENING')

    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, primary_key=True, related_name='state')
    current_rate = models.CharField(max_length=50, choices=Rate.choices)
    fare = models.FloatField(blank=True, null=True, default=None)
    parking_price = models.FloatField(blank=True, null=True, default=None)
    reservation_price = models.FloatField(blank=True, null=True, default=None)

    def clean(self):
        if self.fare and self.fare <= 0:
            raise Exception('Fare must be positive')
        if self.parking_price and self.parking_price < 0:
            raise Exception('Parking price cannot be negative')
        if self.reservation_price and self.reservation_price <= 0.0:
            raise Exception('Reservation price must be positive')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.trip


class TripEvent(models.Model):
    class Event(models.TextChoices):
        start = ('start', 'START')
        end = ('end', 'END')
        parking = ('parking', 'PARKING')
        fueling = ('fueling', 'FUELING')
        washing = ('washing', 'WASHING')
        driving = ('driving', 'DRIVING')

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='events')
    event = models.CharField(max_length=50, choices=Event.choices)
    timestamp = models.DateTimeField(default=timezone.now)
    credentials = models.CharField(max_length=50, blank=True, null=True, default=None)
    cost = models.FloatField(blank=True, null=True, default=None)

    def clean(self):
        if self.cost and self.cost <= 0:
            raise Exception('Cost must be positive')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.trip}, event:{self.event}'
