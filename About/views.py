from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def driver_about(request):
    return render(request, 'driver_about.html')


def ride_owner_about(request):
    return HttpResponse("Ride Owner About")
    # return render(request, 'ride_owner_about.html')


def ride_sharer_about(request):
    return HttpResponse("Ride Sharer About")
    # return render(request, 'ride_sharer_about.html')


def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')
