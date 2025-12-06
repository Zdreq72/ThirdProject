from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Property
from django.db.models import Q
from .models import Favorite
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from inquiries.models import Inquiry, InquiryReply



def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = property.is_favorited_by(request.user)

    inquiries = property.inquiries.select_related("sender").order_by("-created_at")
    replies = InquiryReply.objects.filter(inquiry__property=property).order_by('created_at')


    related_properties = Property.objects.filter(
        Q(city=property.city) | 
        Q(property_type=property.property_type) |
        Q(price__range=(float(property.price) * 0.8, float(property.price) * 1.2))
    ).exclude(pk=pk).distinct().order_by('?')[:3]

    context = {
        'property': property,
        'related_properties': related_properties,
        'inquiries': inquiries,
        'replies': replies,  
        'is_favorited': is_favorited,
    }
    return render(request, 'properties/property.html', context)

@login_required
def toggle_favorite(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    favorite = Favorite.objects.filter(user=request.user, property=property_obj).first()

    if favorite:
        favorite.delete()
        messages.success(request, "Removed from favorites.")
    else:
        Favorite.objects.create(user=request.user, property=property_obj)
        messages.success(request, "Added to favorites.")

    return redirect('properties:detail', pk=pk)


@login_required
def remove_favorite(request, fav_id):
    favorite = get_object_or_404(Favorite, id=fav_id, user=request.user)
    favorite.delete()
    messages.success(request, "Property removed from favorites.")
    return redirect('users:profile')


def is_admin(user):
    return user.is_authenticated and user.is_staff


def add_property(request):
    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST.get('title')
        property_type = request.POST.get('property_type')
        price = request.POST.get('price')
        description = request.POST.get('description')
        city = request.POST.get('city')
        district = request.POST.get('district')
        location = request.POST.get('location')
        area = request.POST.get('area')
        rooms = request.POST.get('rooms')
        bathrooms = request.POST.get('bathrooms')
        age = request.POST.get('age')
        deed_number = request.POST.get('deed_number')

        main_image = request.FILES.get('main_image')
        title_deed = request.FILES.get('title_deed')
        ownership_proof = request.FILES.get('ownership_proof')
        building_license = request.FILES.get('building_license')

        property_obj = Property.objects.create(
            owner=request.user,
            title=title,
            property_type=property_type,
            price=price,
            description=description,
            city=city,
            district=district,
            location=location,
            area=area,
            rooms=rooms,
            bathrooms=bathrooms,
            age=age,
            deed_number=deed_number,
            main_image=main_image,
            title_deed=title_deed,
            ownership_proof=ownership_proof,
            building_license=building_license,
            verification_status='pending',
            purpose=request.POST.get("purpose"),
            status="available",  

        )


        subject = f'New Property Listing Request: {property_obj.title}'
        message = f'A new property has been submitted by {request.user.username}.\n\nProperty: {property_obj.title}\nDeed Number: {property_obj.deed_number}\n\nPlease review it in the admin dashboard.'
        
        send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL], fail_silently=False)

        messages.success(request, 'Property submitted successfully! It is under review.')
        return redirect('main:home')

    context = {
        'types': Property.PROPERTY_TYPE_CHOICES,
        'cities': Property.CITIES
    }

    return render(request, 'properties/add_property.html', context)


@user_passes_test(is_admin)
def admin_dashboard(request):
    pending_properties = Property.objects.filter(verification_status='pending').order_by('-created_at')
    return render(request, 'properties/admin_dashboard.html', {'properties': pending_properties})


@user_passes_test(is_admin)
def verify_property(request, pk, action):
    property_obj = get_object_or_404(Property, pk=pk)
    
    user_email = property_obj.owner.email
    owner_name = property_obj.owner.first_name or property_obj.owner.username
    
    if action == 'approve':
        property_obj.verification_status = 'approved'
        property_obj.save()
        
        subject = f'Congratulations! Your property "{property_obj.title}" is Live'
        message = f'Hello {owner_name},\n\nGreat news! Your property "{property_obj.title}" has been reviewed and APPROVED.\nIt is now visible to all users on SaudiEstate.\n\nThank you.'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
        
        messages.success(request, f'Property "{property_obj.title}" has been approved and user notified.')

    elif action == 'reject':
        property_obj.verification_status = 'rejected'
        property_obj.save()
        
        subject = f'Update regarding your property "{property_obj.title}"'
        message = f'Hello {owner_name},\n\nWe regret to inform you that your property "{property_obj.title}" has been REJECTED after review.\nPlease ensure all information and documents are correct and try again.\n\nRegards,\nSaudiEstate Team.'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)

        messages.warning(request, f'Property "{property_obj.title}" has been rejected and user notified.')
    
    return redirect('properties:admin_dashboard')


def all_properties(request):
    properties = Property.objects.filter(
        verification_status='approved',
        status='available'  
    )

    sort_by = request.GET.get('sort')
    if sort_by == "price_low":
        properties = properties.order_by('price')
    elif sort_by == "price_high":
        properties = properties.order_by('-price')
    elif sort_by == "newest":
        properties = properties.order_by('-created_at')
    elif sort_by == "oldest":
        properties = properties.order_by('created_at')

    prop_type = request.GET.get('type')
    if prop_type:
        properties = properties.filter(property_type=prop_type)

    purpose = request.GET.get('purpose')
    if purpose:
        properties = properties.filter(purpose=purpose)

    show_favs = request.GET.get('favorites')
    if show_favs == "1" and request.user.is_authenticated:
        properties = properties.filter(favorited_by__user=request.user)

    return render(request, 'properties/all_properties.html', {
        'properties': properties,
    })
@login_required
def edit_property(request, pk):

    if request.user.is_staff:
        property_obj = get_object_or_404(Property, pk=pk)
    else:
        property_obj = get_object_or_404(Property, pk=pk, owner=request.user)

    if request.method == 'POST':
        property_obj.title = request.POST.get('title')
        property_obj.description = request.POST.get('description')
        property_obj.price = request.POST.get('price')
        property_obj.area = request.POST.get('area')
        property_obj.rooms = request.POST.get('rooms')
        property_obj.bathrooms = request.POST.get('bathrooms')
        property_obj.age = request.POST.get('age')
        property_obj.purpose = request.POST.get('purpose')
        property_obj.status = request.POST.get('status')
        property_obj.city = request.POST.get('city')
        property_obj.district = request.POST.get('district')
        property_obj.location = request.POST.get('location')

        if 'main_image' in request.FILES:
            property_obj.main_image = request.FILES['main_image']

        property_obj.save()

        messages.success(request, "Property updated successfully!")
        return redirect('users:profile')

    return render(request, 'properties/edit_property.html', {"property": property_obj})
