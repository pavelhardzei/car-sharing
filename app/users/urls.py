from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.UserRegister.as_view(), name='signup'),
    path('users/', views.UserList.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('auth/', views.AuthToken.as_view(), name='get_token')
]
