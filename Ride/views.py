from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def myrides(request):
    return render(request, 'myrides.html')

def setting(request):
    return render(request, 'setting.html')


def request_ride(request):
    return HttpResponse("request ride")