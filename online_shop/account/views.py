from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email)
        print(password)
    
        user = authenticate(request, email = email, password = password)
        print("Authentication Result:", user)

        if user is not None:
            login(request, user)
            return redirect('shop:home')
        
        else:
            messages.error(request, "Invalid Username or Password")
            return render(request, 'account/login.html')

    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('shop:home')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email = email).exists():
            messages.error(request, "Email already registered! Please use a different Email")
            return render(request, 'account/register.html')
        

        user = User.objects.create_user(username=username, email=email, password=password)
        authenticated_user = authenticate(request, email = email, password = password)
        login(request, authenticated_user)
        return redirect('shop:home')

    return render(request, 'account/register.html')