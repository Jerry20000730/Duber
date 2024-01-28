from django.urls import path

from Ride import views

urlpatterns = [
    # login
    path('myrides/', views.myrides, name='myrides'),
    path('request_ride/', views.request_ride, name='request_ride'),
]
