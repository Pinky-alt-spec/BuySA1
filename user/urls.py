from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_profile, name='user_profile'),
    path('user_update/', views.user_update, name='user_update'),
    path('password/', views.password_update, name='password_update'),
    path('orders/', views.user_orders, name='user_orders'),
    path('orders_product/', views.user_order_product, name='user_orders_product'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_order_detail'),
    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.user_delete_comment, name='user_delete_comment'),
]
