from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('trip', views.TripViewSet)
router.register('tripstate', views.TripStateViewSet)
router.register('tripevent', views.TripEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tripmanagement/', views.TripManagement.as_view(), name='management'),
    path('tripmanagement/history/', views.TripsHistory.as_view(), name='history'),
    path('tripmaintenance/', views.TripMaintenance.as_view(), name='maintenance'),
    path('tripmanagement/cost/', views.TripCost.as_view(), name='cost'),
    path('tripmanagement/end/', views.TripEnd.as_view(), name='trip_end')
]
