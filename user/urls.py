from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user_update/', views.user_update, name='user_update'),
    path('address_update/', views.address_update, name='address_update'),
    path('password/', views.password_update, name='password_update'),
]
