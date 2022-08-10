from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('api', views.api, name="api"),
    path('header-demo', views.api, name="api")
]
