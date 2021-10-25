from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name='users'),
    re_path(r'^(?P<pk>(\d+|me))/$', views.UserDetail.as_view(), name='user_detail'),
    re_path(r'^change_password/(?P<pk>(\d+|me))/$', views.ChangePassword.as_view(), name='change_password'),
    re_path(r'^update_user/(?P<pk>(\d+|me))/$', views.UpdateUser.as_view(), name='update_user'),
    path('auth/', views.AuthToken.as_view(), name='get_token')
]
