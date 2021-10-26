from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name='users'),
    re_path(r'^(?P<pk>(\d+|me))/$', views.UserDetail.as_view(), name='user_detail'),
    path('auth/', views.AuthToken.as_view(), name='get_token')
]
