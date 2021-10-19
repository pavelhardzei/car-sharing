from django.urls import path
from . import views

urlpatterns = [
    path('', views.TripManagement.as_view(), name='management'),
    path('history/', views.TripsHistory.as_view(), name='history'),
    path('cost/', views.TripCost.as_view(), name='cost'),
    path('end/', views.TripEnd.as_view(), name='trip_end')
]
