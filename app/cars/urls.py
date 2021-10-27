from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('list', views.CarViewSet, basename='cars')
router.register('carinfo', views.CarInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('available/', views.AvailableCars.as_view(), name='available_cars')
]
