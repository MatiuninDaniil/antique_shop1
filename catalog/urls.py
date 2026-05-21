from django.urls import path
from . import views

urlpatterns = [
    path("",                    views.catalog,     name="catalog"),
    path("item/<str:item_id>/", views.item_detail, name="item_detail"),
    path("contacts/",           views.contacts,    name="contacts"),
]