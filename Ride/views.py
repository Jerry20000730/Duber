from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Account.models import DuberDriver


# Create your views here.
def myrides(request):
    return render(request, 'myrides.html')

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
        'are_you_a_driver':are_you_a_driver,
        'licence_number': licence_number,
        'special_vehicle_info':special_vehicle_info,
        'vehicle_type':vehicle_type,
    }
    return render(request, 'setting.html', context=context)

def request_ride(request):
    return render(request, 'riderequest.html')

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
        return render(request, 'edit_account.html',context=context)
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
        return render(request,'edit_driver.html',context=context)
    

