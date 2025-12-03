from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':

        # ----- Basic fields -----
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        city = request.POST.get('city')

        # ----- Country Code + Phone -----
        country_code = request.POST.get('country_code')
        phone_local = request.POST.get('phone_number')

        if country_code and phone_local:
            full_phone = f"{country_code}{phone_local}"
        else:
            full_phone = phone_local

        # ----- Password -----
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # ----- Validations -----
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('users:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('users:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('users:register')

        if User.objects.filter(phone_number=full_phone).exists():
            messages.error(request, "Phone number already registered!")
            return redirect('users:register')

        try:
            # ----- Create user -----
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Extra fields
            user.city = city
            user.country_code = country_code
            user.phone_number = full_phone

            user.save()

            messages.success(request, f"Account created for {username}!")
            return redirect('users:login')

        except Exception as e:
            messages.error(request, f"Registration error: {e}")
            print("ERROR:", e)
            return redirect('users:register')

    return render(request, 'users/register.html')



def login_user(request):

    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':

        username_val = request.POST.get('username')
        password_val = request.POST.get('password')

        user = authenticate(request, username=username_val, password=password_val)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('main:home')

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'users/login.html')



def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('main:home')
