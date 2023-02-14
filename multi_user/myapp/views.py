from django.shortcuts import render, redirect
from .forms import *
from .models import MyUser
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request,'home.html')

@login_required
def admin_page(request):
    return render(request,'admin.html')

@login_required
def emp_profile(request):
    if request.user.is_employee:
        users = MyUser.objects.all()
        return render(request,'emp_profile.html',{'users':users})
    elif request.user.is_admin:
        users = MyUser.objects.all()
        return render(request,'emp_profile.html',{'users':users})
    else:
        return redirect('home')


def cust_registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = Cust_RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                is_customer = form.cleaned_data['is_customer']
                user = authenticate(email=email, username=username, password1=password, is_customer=is_customer)
                return redirect('login')
        else:
            form = Cust_RegistrationForm()
            return render(request, 'cust_registration.html', {'form':form})
    else:
        return redirect('home')


def emp_registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = Emp_RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                is_employee = form.cleaned_data['is_employee']
                user = authenticate(email=email, username=username, password1=password, is_employee=is_employee)
                return redirect('login')
        else:
            form = Emp_RegistrationForm()
            return render(request, 'emp_registration.html', {'form':form})
    else:
        return redirect('emp_profile')

def login_func(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            # if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None and user.is_customer:
                login(request, user)
                return redirect('home')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('emp_profile')
            elif user is not None and user.is_admin:
                login(request, user)
                return redirect('admin_page')
        else:
            form = LoginForm()
            return render(request, 'login.html', {'form':form})
    else:
        return redirect('emp_profile')


def logout_func(request):
    logout(request)
    return redirect('home')