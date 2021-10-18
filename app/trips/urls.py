from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('list', views.TripViewSet)
router.register('states', views.TripStateViewSet)
router.register('events', views.TripEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('management/', views.TripManagement.as_view(), name='management'),
    path('management/history/', views.TripsHistory.as_view(), name='history'),
    path('maintenance/', views.TripMaintenance.as_view(), name='maintenance'),
    path('management/cost/', views.TripCost.as_view(), name='cost'),
    path('management/end/', views.TripEnd.as_view(), name='trip_end')
]
