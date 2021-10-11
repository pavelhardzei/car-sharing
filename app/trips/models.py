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

    def __str__(self):
        return str(self.trip)


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

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.trip}, event:{self.event}'
