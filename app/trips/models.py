from django.db import models
from django.utils import timezone
from users.models import UserAccount
from cars.models import Car


class Trip(models.Model):
    car = models.ForeignKey(Car, null=True, default=None, on_delete=models.CASCADE, related_name='trips')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='trips')
    total_cost = models.FloatField(null=True, default=None)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, default=None)
    total_distance = models.IntegerField(null=True, default=None)
    reservation_time = models.IntegerField(null=True, default=None)

    def __str__(self):
        return f'id:{self.id}, car:{self.car}, user:{self.user}'


class TripState(models.Model):
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, primary_key=True, related_name='state')
    current_rate = models.CharField(max_length=50)
    fare = models.FloatField(null=True, default=None)
    parking_price = models.FloatField(null=True, default=None)
    reservation_price = models.FloatField(null=True, default=None)

    def __str__(self):
        return self.trip


class TripEvent(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='events')
    event = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)
    credentials = models.CharField(max_length=50, null=True, default=None)
    cost = models.FloatField(null=True, default=None)

    def __str__(self):
        return f'{self.trip}, event:{self.event}'
