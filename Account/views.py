from django.contrib import messages, auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from Account.forms import DuberUserRegistrationForm
from Account.models import DuberUser


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('myrides')
        else:
            messages.add_message(request, messages.ERROR, mark_safe("Invalid login credentials<br/>Please try again!"))
            return redirect('login')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = DuberUserRegistrationForm(request.POST)
        print(form.is_bound)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password1']

            user = DuberUser.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password
            )
            user.save()
            messages.add_message(request, messages.SUCCESS, "You may now proceed to login")
            return redirect('login')
        else:
            for id in form.errors:
                messages.add_message(request, messages.ERROR, form.errors[id].as_text())
            return redirect('register')
    else:
        form = DuberUserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'signup.html', context=context)

def logout(request):
    logout(request)
    response = redirect(redirect('login'))
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response
