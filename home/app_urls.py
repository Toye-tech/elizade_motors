from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/cars/', views.api_cars_list, name='api_cars_list'),
    path('api/cars/create/', views.api_car_create, name='api_car_create'),
    path('api/cars/<int:car_id>/update/', views.api_car_update, name='api_car_update'),
    path('api/cars/<int:car_id>/delete/', views.api_car_delete, name='api_car_delete'),
    path('api/cars/<int:car_id>/toggle/', views.api_car_toggle, name='api_car_toggle'),
]
path('api/cars/',
         views.api_cars_list,
         name='api_cars_list'),

path('api/cars/create/',
         views.api_car_create,
         name='api_car_create'),

path('api/cars/<int:car_id>/update/',
         views.api_car_update,
         name='api_car_update'),

path('api/cars/<int:car_id>/delete/',
         views.api_car_delete,
         name='api_car_delete'),

path('api/cars/<int:car_id>/toggle/',
         views.api_car_toggle,
         name='api_car_toggle'),
