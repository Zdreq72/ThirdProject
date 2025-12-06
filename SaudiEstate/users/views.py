from urllib import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required
from properties.models import Property, Favorite
from inquiries.models import Inquiry, VisitRequest 
from django.views.decorators.csrf import csrf_protect



def register(request):
    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':
        data = request.POST.copy()  

        username = data.get('username')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        city = data.get('city')
        national_id = data.get('national_id')
        country_code = data.get('country_code')
        phone_local = data.get('phone_number')
        full_phone = f"{country_code}{phone_local}" if country_code and phone_local else phone_local
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'users/register.html', {"form_data": data})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'users/register.html', {"form_data": data})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'users/register.html', {"form_data": data})

        if User.objects.filter(phone_number=full_phone).exists():
            messages.error(request, "Phone number already registered!")
            return render(request, 'users/register.html', {"form_data": data})

        if User.objects.filter(national_id=national_id).exists():
            messages.error(request, "National ID already registered!")
            return render(request, 'users/register.html', {"form_data": data})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.city = city
        user.country_code = country_code
        user.phone_number = full_phone
        user.national_id = national_id
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect('users:login')

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


@login_required
def user_profile(request):
    user = request.user

    my_properties = Property.objects.filter(owner=user)
    favorites = Favorite.objects.filter(user=user).select_related("property")

    inquiries = Inquiry.objects.filter(sender=user).select_related("property")

    received_inquiries = Inquiry.objects.filter(property__owner=user).select_related("property", "sender")

    visit_requests = VisitRequest.objects.filter(requester=user).select_related("property")

    context = {
        "user": user,
        "my_properties": my_properties,
        "favorites": favorites,
        "inquiries": inquiries,
        "received_inquiries": received_inquiries,  
        "visit_requests": visit_requests,
    }

    return render(request, "users/user_profile.html", context)


@csrf_protect
@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        national_id = request.POST.get('national_id')
        phone_local = request.POST.get('phone_number')
        country_code = request.POST.get('country_code')
        full_phone = f"{country_code}{phone_local}" if country_code and phone_local else phone_local

        if User.objects.exclude(id=user.id).filter(national_id=national_id).exists():
            messages.error(request, "National ID is already registered.")
            return render(request, "users/edit_profile.html", {"user": user, "form_data": request.POST})

        if User.objects.exclude(id=user.id).filter(phone_number=full_phone).exists():
            messages.error(request, "Phone number is already registered.")
            return render(request, "users/edit_profile.html", {"user": user, "form_data": request.POST})

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.city = request.POST.get('city')
        user.national_id = national_id
        user.country_code = country_code
        user.phone_number = full_phone

        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('users:profile')

    return render(request, 'users/edit_profile.html', {"user": user})


def profile(request):
    inquiries_sent = Inquiry.objects.filter(sender=request.user)
    
    received_inquiries = Inquiry.objects.filter(property__owner=request.user)

    return render(request, "users/profile.html", {
        "inquiries": inquiries_sent,
        "received_inquiries": received_inquiries,
    })    

