from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('cars/', views.CarList.as_view(), name='cars'),
    path('carinfos/', views.CarInfoList.as_view(), name='car_infos')
]
