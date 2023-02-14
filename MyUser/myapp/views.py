from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from .models import MyUser
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request,'home.html')

@login_required
def profile(request):
    users = MyUser.objects.all()
    return render(request,'profile.html',{'users':users})


def registration_func(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(email=email, username=username, password1=password)
                return redirect('login')
        else:
            form = RegistrationForm()
            return render(request, 'registration.html', {'form':form})
    else:
        return redirect('profile')

def login_func(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            # if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
        else:
            form = LoginForm()
            return render(request, 'login.html', {'form':form})
    else:
        return redirect('profile')

def logout_func(request):
    logout(request)
    return redirect('home')