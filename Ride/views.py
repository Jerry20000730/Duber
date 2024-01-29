from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from Ride.forms import DuberRideRequestForm


# Create your views here.
def myrides(request):
    return render(request, 'myrides.html')


def setting(request):
    return render(request, 'setting.html')


def request_ride(request):
    if request.method == 'POST':
        print(request.POST)
    else:
        form = DuberRideRequestForm()
        context = {
            'form': form
        }
        return render(request, 'riderequest.html', context=context)


def edit_account(request):
    return render(request, 'edit_account.html')


def edit_driver(request):
    return render(request, 'edit_driver.html')
