from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('trip', views.TripViewSet)
router.register('tripstate', views.TripStateViewSet)
router.register('tripevent', views.TripEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tripmanagement/', views.TripManagement.as_view(), name='booking')
]