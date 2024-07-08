from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        full_name = request.POST['full_name']
        telephone = request.POST['telephone']
        password = request.POST['password']
        password2 = request.POST['password2']
        profile_image = request.FILES.get('profile_image')

        if password != password2:
            return render(request, 'core/register.html', {'error': 'Passwords do not match'})

        user = CustomUser.objects.create(
            username=username,
            email=email,
            full_name=full_name,
            telephone=telephone,
            profile_image=profile_image,
            password=make_password(password)
        )
        login(request, user)
        return redirect('login')

    return render(request, 'core/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            form_errors = "Invalid username or password. Please try again."
            return render(request, 'core/login.html', {'form_errors': form_errors})

    return render(request, 'core/login.html')

@login_required
def home(request):
    return render(request, 'core/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('home')