from django.urls import path

from Ride import views

urlpatterns = [
    # login
    path('myrides/', views.myrides, name='myrides'),
    path('setting/', views.setting, name='setting'),
    path('request_ride/', views.request_ride, name='request_ride'),
    path('edit_account/',views.edit_account,name='edit_account'),
    path('edit_driver/',views.edit_driver,name='edit_driver'),
    path('ride_detail/<uuid:pk>',views.ride_detail,name='ride_detail'),
]
