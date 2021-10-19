from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('list', views.TripViewSet)
router.register('states', views.TripStateViewSet)
router.register('events', views.TripEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('management/', include('trips.management_urls')),
    path('maintenance/', views.TripMaintenance.as_view(), name='maintenance')
]
