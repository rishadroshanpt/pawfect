from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('register',views.register),
    path('shop_home',views.shop_home),
    path('logout',views.shp_logout),
    # path('add_category',views.add_category),
    path('add_pet',views.add_pet),
    path('delete_pet/<pid>',views.delete_pet),
    path('edit_pet/<pid>',views.edit_pet),
    path('delete_category/<pid>',views.delete_category),
    path('edit_category/<pid>',views.edit_category),
    path('add_prod',views.add_prod),
    path('details/<pid>',views.details,name="details"),
    path('edit_prod/<pid>',views.edit_prod),
    path('edit_details/<pid>',views.edit_details,name="edit_details"),
    path('delete_details/<pid>',views.delete_details),
    path('delete_prod/<pid>',views.delete_prod),
    # path('bookings',views.bookings),

    # -------------------------------user-----------------------------

    path('user_home',views.user_home),
    path('products/<pid>',views.products),
    path('product/<pid>',views.product),
    path('petType/<pid>',views.petType),
    path('addCart/<pid>',views.addCart),
    path('viewCart',views.viewCart),
]