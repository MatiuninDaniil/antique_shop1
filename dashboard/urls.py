from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.overview,            name='dashboard'),
    path('items/',                        views.item_list,           name='dashboard_items'),
    path('items/add/',                    views.item_form,           name='dashboard_item_add'),
    path('items/<str:item_id>/edit/',     views.item_form,           name='dashboard_item_edit'),
    path('items/<str:item_id>/sold/',     views.item_mark_sold,      name='dashboard_item_sold'),
    path('items/<str:item_id>/delete/',   views.item_delete,         name='dashboard_item_delete'),
    path('reservations/',                 views.reservations,        name='dashboard_reservations'),
    path('reservations/<int:pk>/confirm/',views.reservation_confirm, name='dashboard_res_confirm'),
    path('reservations/<int:pk>/cancel/', views.reservation_cancel,  name='dashboard_res_cancel'),
    path('clients/',                      views.clients,             name='dashboard_clients'),
    path('sales/',                        views.sales,               name='dashboard_sales'),
]