from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from Account.models import DuberDriver
from Ride.forms import DuberRideRequestForm
from Ride.models import Ride


# Create your views here.
def myrides(request):
    owner_rides = Ride.objects.filter(owner=request.user)
    if request.user.is_driver:
        driver_rides = Ride.objects.filter(driver=request.user)
    else:
        driver_rides = []
    sharer_rides = Ride.objects.filter(sharer=request.user)
    context = {
        'owner_rides': owner_rides,
        'driver_rides': driver_rides,
        'sharer_rides': sharer_rides,
        'owner_rides_number': len(owner_rides),
        'driver_rides_number': len(driver_rides),
        'sharer_rides_number': len(sharer_rides),
        'my_ride_number': len(owner_rides) + len(driver_rides) + len(sharer_rides),
    }
    return render(request, 'myrides.html', context=context)


def setting(request):
    username = request.user.username
    password = request.user.password
    first_name = request.user.first_name
    last_name = request.user.last_name
    phone_number = request.user.phone_number
    email = request.user.email
    user_driver = DuberDriver.objects.filter(duber_user=username)
    are_you_a_driver = request.user.is_driver
    licence_number = user_driver.values('licence_plate_number').first()
    licence_number = licence_number['licence_plate_number'] if licence_number else None

    special_vehicle_info = user_driver.values('special_info')
    vehicle_type = user_driver.values('vehicle_type').first()
    vehicle_type = vehicle_type['vehicle_type'] if vehicle_type else None
    print(vehicle_type)
    context = {
        'username': username,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'email': email,
        'are_you_a_driver': are_you_a_driver,
        'licence_number': licence_number,
        'special_vehicle_info': special_vehicle_info,
        'vehicle_type': vehicle_type,
    }
    return render(request, 'setting.html', context=context)


def request_ride(request):
    if request.method == 'POST':
        form = DuberRideRequestForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.owner = request.user
            ride.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, "Your ride request has been created in My Rides!")
            return redirect('myrides')
        else:
            mapping = {
                'dst_addr': 'Destination Address',
                'num_passengers_owner_party': 'Desired Number of Passengers',
                'owner_desired_arrival_time': 'Desired Arrival Time',
                'owner_desired_vehicle_type': 'Desired Vehicle Type',
                'is_shareable': 'Is the ride shareable',
            }
            for id in form.errors:
                if id != '__all__':
                    messages.add_message(request, messages.ERROR,
                                         "{}: {}\n".format(mapping[id], form.errors[id].as_text()))
                else:
                    messages.add_message(request, messages.ERROR, "{}\n".format(form.errors[id].as_text()))
            return redirect('request_ride')
    else:
        form = DuberRideRequestForm()
    context = {
        'form': form
    }
    return render(request, 'riderequest.html', context=context)


def edit_account(request):
    if request.method == 'GET':
        username = request.user.username
        password = request.user.password
        first_name = request.user.first_name
        last_name = request.user.last_name
        phone_number = request.user.phone_number
        email = request.user.email
        context = {
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'email': email,
        }
        return render(request, 'edit_account.html', context=context)
    else:
        new_first_name = request.POST['first_name']
        new_last_name = request.POST['last_name']
        new_phone_number = request.POST['phone_number']
        new_email = request.POST['email']

        user_model = get_user_model()
        user_model.objects.filter(username=request.user.username).update(first_name=new_first_name)
        user_model.objects.filter(username=request.user.username).update(last_name=new_last_name)
        user_model.objects.filter(username=request.user.username).update(phone_number=new_phone_number)
        user_model.objects.filter(username=request.user.username).update(email=new_email)

        return redirect('setting')


def edit_driver(request):
    if request.method == 'GET':
        username = request.user.username
        user_driver = DuberDriver.objects.filter(duber_user=username)
        are_you_a_driver = request.user.is_driver
        licence_number = user_driver.values('licence_plate_number')
        special_vehicle_info = user_driver.values('special_info')
        context = {
            'username': username,
            'are_you_a_driver': are_you_a_driver,
            'licence_number': licence_number,
            'special_vehicle_info': special_vehicle_info,
        }
        return render(request, 'edit_driver.html', context=context)


def ride_detail(request, pk):
    ride = Ride.objects.filter(ride_id=pk).first()
    owner = get_user_model().objects.filter(username=ride.owner).first()
    if ride.driver is not None:
        driver = DuberDriver.objects.filter(duber_user=ride.driver).first()
    else:
        driver = None
    if ride.sharer is not None:
        sharer = get_user_model().objects.filter(username=ride.sharer).all()
    else:
        sharer = None
    context = {
        'ride': ride,
        'owner': owner,
        'status': ride.status,
        'driver': driver,
        'sharer': sharer,
    }
    return render(request, 'myride_detail.html', context=context)
