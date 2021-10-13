from django.contrib import admin
from .models import Trip, TripState, TripEvent

admin.site.register(Trip)
admin.site.register(TripState)
admin.site.register(TripEvent)
