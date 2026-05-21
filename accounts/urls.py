from django.urls import path
from . import views

urlpatterns = [
    path('register/',               views.register_view,      name='register'),
    path('login/',                  views.login_view,         name='login'),
    path('logout/',                 views.logout_view,        name='logout'),
    path('cart/',                   views.cart_view,          name='cart_view'),
    path('cart/add/<str:item_id>/', views.cart_add,           name='cart_add'),
    path('cart/remove/<str:item_id>/', views.cart_remove,     name='cart_remove'),
    path('reserve/<str:item_id>/',  views.reserve,            name='reserve'),
    path('reservations/',           views.my_reservations,    name='my_reservations'),
    path('reservations/<str:code>/', views.reservation_detail, name='reservation_detail'),
]