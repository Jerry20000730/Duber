from django.shortcuts import render

# Create your views here.
def myrides(request):
    return render(request, 'myrides.html')