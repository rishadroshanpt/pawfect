from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('shop_home',views.shop_home),
    path('logout',views.shp_logout),
    path('add_category',views.add_category),
    path('add_pet',views.add_pet),
    path('add_prod',views.add_prod),
    path('details',views.details),
    path('edit_prod/<pid>',views.edit_prod),
    path('delete_prod/<pid>',views.delete_prod),
    # path('bookings',views.bookings),
]