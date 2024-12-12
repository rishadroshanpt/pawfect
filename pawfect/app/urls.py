from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('shop_home',views.shop_home),
    path('logout',views.shp_logout),
    path('add_prod',views.add_prod),
    path('edit_prod/<pid>',views.edit_prod),
    path('delete_prod/<pid>',views.delete_prod),
    path('bookings',views.bookings),
]