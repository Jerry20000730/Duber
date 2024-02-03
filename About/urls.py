from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('driver/', views.driver_about, name='driver_about'),
    path('ride_owner/', views.ride_owner_about, name='ride_owner_about'),
    path('ride_sharer/', views.ride_sharer_about, name='ride_sharer_about'),
    path('contact/', views.contact, name='contact'),
]