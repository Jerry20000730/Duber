from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from Account.models import DuberDriver
from Duber.settings import RideStatus
from Ride.forms import DuberRideRequestForm, RoleBasedFilteringForm
from Ride.models import Ride


# Create your views here.
@login_required(login_url='/account/login')
def myrides(request):
    if request.method == "GET":
        initial_data = {'role': ['owner', 'driver', 'sharer']}
        form = RoleBasedFilteringForm(initial_data)
        owner_rides = Ride.objects.filter(owner=request.user)
        if request.user.is_driver:
            driver = DuberDriver.objects.filter(duber_user=request.user).first()
            driver_rides = Ride.objects.filter(driver=driver)
        else:
            driver_rides = []
        sharer_rides = Ride.objects.filter(sharer=request.user).all()
        context = {
            'form': form,
            'owner_rides': owner_rides,
            'driver_rides': driver_rides,
            'sharer_rides': sharer_rides,
            'owner_rides_number': len(owner_rides),
            'driver_rides_number': len(driver_rides),
            'sharer_rides_number': len(sharer_rides),
            'my_ride_number': len(owner_rides) + len(driver_rides) + len(sharer_rides),
        }
        return render(request, 'myrides.html', context=context)
    else:
        form = RoleBasedFilteringForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            owner_rides = Ride.objects.filter(owner=request.user)
            if request.user.is_driver:
                driver = DuberDriver.objects.filter(duber_user=request.user).first()
                driver_rides = Ride.objects.filter(driver=driver)
            else:
                driver_rides = []
            sharer_rides = Ride.objects.filter(sharer=request.user).all()
            if 'owner' not in role:
                owner_rides = []
            if 'driver' not in role:
                driver_rides = []
            if 'sharer' not in role:
                sharer_rides = []
            current_data = form.cleaned_data
            form = RoleBasedFilteringForm(current_data)
            context = {
                'form': form,
                'owner_rides': owner_rides,
                'driver_rides': driver_rides,
                'sharer_rides': sharer_rides,
                'owner_rides_number': len(owner_rides),
                'driver_rides_number': len(driver_rides),
                'sharer_rides_number': len(sharer_rides),
                'my_ride_number': len(owner_rides) + len(driver_rides) + len(sharer_rides),
            }
            return render(request, 'myrides.html', context=context)



def join_ride(request, pk, num_passenger_sharer_party):
    if request.method == "GET":
        ride = Ride.objects.get(ride_id=pk)
        sharer_user = get_user_model().objects.get(username=request.user.username)
        ride.sharer.add(sharer_user)
        # update to the ride table
        current_sharer_num = Ride.objects.get(ride_id=pk).num_passengers_sharer_party
        Ride.objects.filter(ride_id=pk).update(num_passengers_sharer_party=num_passenger_sharer_party+current_sharer_num)
        messages.add_message(request, messages.SUCCESS, 'You have successfully joined a ride')
        return redirect('myrides')


def sharer_search_result(request):
    if request.method == 'POST':
        new_dst_addr = request.POST.get('dst_addr')
        arrival_window_first = request.POST.get('arrival_window_first')
        arrival_window_second = request.POST.get('arrival_window_second')
        num_passenger_sharer_party = request.POST.get('num_passenger_sharer_party')

        rides = Ride.objects.filter(
            Q(dst_addr=new_dst_addr) &
            Q(owner_desired_arrival_time__gte=arrival_window_first) &
            Q(owner_desired_arrival_time__lte=arrival_window_second) &
            Q(status=RideStatus.OPEN) &
            ~Q(driver_id__isnull=True) &
            Q(is_shareable=True) &
            Q(num_passengers_owner_party__lte=F('driver__maximum_passenger_number') - num_passenger_sharer_party - F('num_passengers_owner_party'))
        )
        return render(request, 'sharer_search_result.html',
                      context={'rides': rides, 'num_passenger_sharer_party': num_passenger_sharer_party})
    else:
        return redirect('sharer_search_result')


def search_ride_sharer(request):
    return render(request, 'search_ride_sharer.html')


@login_required(login_url='/account/login')
def setting(request):
    # Account Info
    username = request.user.username
    password = request.user.password
    first_name = request.user.first_name
    last_name = request.user.last_name
    phone_number = request.user.phone_number
    email = request.user.email

    # Driver Info
    user_driver = DuberDriver.objects.filter(duber_user=username)
    are_you_a_driver = request.user.is_driver

    maximum_passenger_number = user_driver.values_list('maximum_passenger_number').first()
    maximum_passenger_number = maximum_passenger_number[0] if maximum_passenger_number else None

    licence_number = user_driver.values('licence_plate_number').first()
    licence_number = licence_number['licence_plate_number'] if licence_number else None

    special_vehicle_info = user_driver.values('special_info').first()
    special_vehicle_info = special_vehicle_info['special_info'] if special_vehicle_info else None

    vehicle_type = user_driver.values('vehicle_type').first()

    vehicle_type = vehicle_type['vehicle_type'] if vehicle_type else None

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
        'maximum_passenger_number': maximum_passenger_number,
    }
    return render(request, 'setting.html', context=context)


@login_required(login_url='/account/login')
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


@login_required(login_url='/account/login')
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


@login_required(login_url='/account/login')
def edit_driver(request):
    if request.method == 'GET':
        # Driver Info
        username = request.user.username
        user_driver = DuberDriver.objects.filter(duber_user=username)
        are_you_a_driver = request.user.is_driver

        maximum_passenger_number = user_driver.values_list('maximum_passenger_number').first()
        maximum_passenger_number = maximum_passenger_number[0] if maximum_passenger_number else None

        licence_number = user_driver.values('licence_plate_number').first()
        licence_number = licence_number['licence_plate_number'] if licence_number else None

        special_vehicle_info = user_driver.values('special_info').first()
        special_vehicle_info = special_vehicle_info['special_info'] if special_vehicle_info else None

        vehicle_type = user_driver.values('vehicle_type').first()
        vehicle_type = vehicle_type['vehicle_type'] if vehicle_type else None

        context = {
            'username': username,
            'are_you_a_driver': are_you_a_driver,
            'licence_number': licence_number,
            'special_vehicle_info': special_vehicle_info,
            'vehicle_type': vehicle_type,
            'maximum_passenger_number': maximum_passenger_number,
        }
        return render(request, 'edit_driver.html', context=context)
    else:
        new_identity = request.POST['are_you_a_driver']

        if (new_identity == "121"):
            new_identity = True
        else:
            new_identity = False

        if (new_identity == True):
            new_vehicle_type = request.POST['vehicle_type']
            new_maximum_passenger_number = request.POST['maximum_number_of_passengers']
            new_licence_number = request.POST['licence_number']
            new_special_vehicle_info = request.POST['special_vehicle_info']

        user_model = get_user_model()
        user_model.objects.filter(username=request.user.username).update(is_driver=new_identity)

        current_username = request.user.username
        duber_user = user_model.objects.filter(username=current_username).first()
        if (new_identity == True):
            exists = DuberDriver.objects.filter(duber_user=duber_user).exists()
            if (exists):
                new_driver = DuberDriver.objects.filter(duber_user=duber_user)
                new_driver.update(vehicle_type=new_vehicle_type)
                new_driver.update(licence_plate_number=new_licence_number)
                new_driver.update(maximum_passenger_number=new_maximum_passenger_number)
                new_driver.update(special_info=new_special_vehicle_info)
            else:
                new_driver = DuberDriver.objects.create(duber_user=duber_user)

                new_driver.vehicle_type = new_vehicle_type
                new_driver.licence_plate_number = new_licence_number
                new_driver.maximum_passenger_number = new_maximum_passenger_number
                new_driver.special_info = new_special_vehicle_info
                new_driver.save()
        else:
            DuberDriver.objects.filter(duber_user=request.user.username).delete()

        return redirect('setting')


@login_required(login_url='/account/login')
def ride_detail(request, pk):
    ride = Ride.objects.filter(ride_id=pk).first()
    owner = get_user_model().objects.filter(username=ride.owner).first()
    if ride.driver is not None:
        driver = DuberDriver.objects.filter(duber_user=ride.driver).first()
        driver_user = driver.duber_user
    else:
        driver = None
        driver_user = None
    if ride.sharer is not None:
        sharer = ride.sharer.all()
    else:
        sharer = None
    context = {
        'ride': ride,
        'owner': owner,
        'status': ride.status,
        'driver': driver,
        'driver_user': driver_user,
        'sharer': sharer,
    }

    return render(request, 'myride_detail.html', context=context)


@login_required(login_url='/account/login')
def edit_detail(request, pk):
    if request.method == 'GET':
        ride = Ride.objects.filter(ride_id=pk).first()
        owner = get_user_model().objects.filter(username=ride.owner).first()
        if ride.driver is not None:
            driver = DuberDriver.objects.filter(duber_user=ride.driver).first()
            driver_user = DuberDriver.objects.filter(duber_user=driver.duber_user).first()
        else:
            driver = None
            driver_user = None
        if ride.sharer is not None:
            sharer = get_user_model().objects.filter(username=ride.sharer).all()
        else:
            sharer = None
        context = {
            'ride': ride,
            'owner': owner,
            'status': ride.status,
            'driver': driver,
            'driver_user': driver_user,
            'sharer': sharer,
        }
        return render(request, 'edit_detail.html', context=context)
    else:
        new_ride_destination = request.POST.get('ride_destination')
        new_desired_arrival_time_owner = request.POST.get('desired_arrival_time_owner')

        new_passenger_number_owner = request.POST.get('passenger_number_owner')
        new_shareable = request.POST.get('shareable')
        if (new_shareable == "1"):
            new_shareable = True
        else:
            new_shareable = False
        new_desired_vehicle_type = request.POST.get('desired_vehicle_type')
        new_special_request = request.POST.get('special_request')

        ride = Ride.objects.filter(ride_id=pk)
        ride.update(dst_addr=new_ride_destination)
        ride.update(owner_desired_arrival_time=new_desired_arrival_time_owner)
        ride.update(num_passengers_owner_party=new_passenger_number_owner)
        ride.update(is_shareable=new_shareable)
        ride.update(owner_desired_vehicle_type=new_desired_vehicle_type)
        ride.update(special_requests=new_special_request)
        ride.update(time_uptate=timezone.now())

        return redirect('ride_detail', pk=pk)


@login_required(login_url='/account/login')
def search_ride(request):
    return render(request, 'search_ride_entry.html')


@login_required(login_url='/account/login')
def search_ride_driver(request):
    if not request.user.is_driver:
        messages.add_message(request, messages.ERROR,
                             "You are not registered as a driver! Click below to register as a driver."
                             "as a driver.")
        return redirect('search_ride')

    driver_duberuser = get_user_model().objects.get(username=request.user.username)
    driver = DuberDriver.objects.filter(duber_user=driver_duberuser).first()

    rides = Ride.objects.annotate(sum_passengers=F('num_passengers_owner_party') + F('num_passengers_sharer_party')) \
        .filter(status=RideStatus.OPEN,
                driver=None,
                sum_passengers__lte=driver.maximum_passenger_number) \
        .filter(Q(owner_desired_vehicle_type__isnull=True) | Q(
        owner_desired_vehicle_type__exact=driver.vehicle_type)) \
        .filter(Q(special_requests__isnull=True) | Q(special_requests__exact='') | Q(
        special_requests__exact=driver.special_info)) \
        .exclude(owner=driver_duberuser)

    context = {
        'rides': rides,
        'res_ride_number': len(rides),
    }
    return render(request, 'search_ride_driver.html', context=context)


@login_required(login_url='/account/login')
def search_ride_sharer(request):
    return render(request, 'search_ride_sharer.html')


@login_required(login_url='/account/login')
def claim_ride_driver(request, pk):
    if not request.user.is_driver:
        messages.add_message(request, messages.ERROR,
                             "You are not registered as a driver! Click below to register as a driver.")
        return redirect('search_ride')

    driver_duberuser = get_user_model().objects.get(username=request.user.username)
    driver = DuberDriver.objects.get(duber_user=driver_duberuser)
    ride = Ride.objects.get(ride_id=pk)
    ride.driver = driver
    ride.save()
    messages.add_message(request, messages.SUCCESS, "You have successfully claimed the ride!")
    return redirect('myrides')


def complete_ride(request, pk):
    Ride.objects.filter(pk=pk).update(status=RideStatus.COMPLETE)
    return redirect('myrides')
