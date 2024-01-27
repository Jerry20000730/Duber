from django.urls import path

from Ride import views

urlpatterns = [
    # login
    path('myrides/', views.myrides, name='myrides'),
]
