from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, VisitRequest , PropertyImage
from django.db.models import Q
from .models import Favorite
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from inquiries.models import Inquiry, InquiryReply 
from datetime import datetime, timedelta, date ,time
from django.http import JsonResponse



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
    status = ''

    if favorite:
        favorite.delete()
        status = 'removed'
        msg = "Removed from favorites."
    else:
        Favorite.objects.create(user=request.user, property=property_obj)
        status = 'added'
        msg = "Added to favorites."

    if request.method == "POST": 
        return JsonResponse({'status': status, 'message': msg})

    messages.success(request, msg)
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
   
        deed_number = request.POST.get('deed_number')
        
        if Property.objects.filter(deed_number=deed_number).exists():
            messages.error(request, "Error: A property with this Deed Number already exists.")
            
            context = {
                'types': Property.PROPERTY_TYPE_CHOICES,
                'cities': Property.CITIES,
                'form_data': request.POST 
            }
            return render(request, 'properties/add_property.html', context)


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
        
        gallery_images = request.FILES.getlist('gallery_images') 
        for image in gallery_images:
            PropertyImage.objects.create(property=property_obj, image=image)

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

    city = request.GET.get('city')
    if city:
        properties = properties.filter(city__iexact=city)


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
        'cities': Property.CITIES,               
        'types': Property.PROPERTY_TYPE_CHOICES, 
        'purposes': Property.PROPERTY_PURPOSE_CHOICES, 

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



@login_required
def book_visit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        if request.user == property_obj.owner:
            messages.error(request, "You cannot book a visit for your own property.")
            return redirect('properties:detail', pk=pk)

        visit_date_str = request.POST.get('visit_date', '').strip()
        visit_time_str = request.POST.get('visit_time', '').strip()

        try:
            visit_date = datetime.strptime(visit_date_str, "%Y-%m-%d").date()
            
            try:
                visit_time = datetime.strptime(visit_time_str, "%H:%M").time()
            except ValueError:
                visit_time = datetime.strptime(visit_time_str, "%H:%M:%S").time()
                
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return redirect('properties:detail', pk=pk)
            
        request_datetime = datetime.combine(visit_date, visit_time)
        if request_datetime < datetime.now():
             messages.error(request, "Cannot book a visit in the past.")
             return redirect('properties:detail', pk=pk)

        start_window = (datetime.combine(date.today(), visit_time) - timedelta(hours=1)).time()
        end_window = (datetime.combine(date.today(), visit_time) + timedelta(hours=1)).time()

        conflict = VisitRequest.objects.filter(
            property=property_obj,
            visit_date=visit_date,
            status='pending',
            visit_time__range=(start_window, end_window)
        ).exists()

        if conflict:
            messages.error(request, "This time slot is already booked. Please choose another time.")
            return redirect('properties:detail', pk=pk)

        VisitRequest.objects.create(
            requester=request.user,
            property=property_obj,
            visit_date=visit_date,
            visit_time=visit_time,
            status='pending'
        )
        
        subject = f"New Visit Request: {property_obj.title}"
        msg = f"User {request.user.username} wants to visit on {visit_date} at {visit_time}.\nPlease check your dashboard to approve or reject."
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [property_obj.owner.email], fail_silently=True)

        messages.success(request, "Visit request sent! Waiting for owner approval.")
        return redirect('properties:detail', pk=pk)

    return redirect('properties:detail', pk=pk)



@login_required
def my_visit_requests(request):
    incoming_requests = VisitRequest.objects.filter(property__owner=request.user).order_by('-created_at')
    my_requests = VisitRequest.objects.filter(requester=request.user).order_by('-created_at')

    return render(request, 'properties/visit_requests.html', {
        'incoming_requests': incoming_requests,
        'my_requests': my_requests
    })


@login_required
def handle_visit_request(request, request_id, action):
    visit_req = get_object_or_404(VisitRequest, pk=request_id, property__owner=request.user)
    
    requester_email = visit_req.requester.email
    prop_title = visit_req.property.title

    if action == 'approve':
        start_window = (datetime.combine(date.today(), visit_req.visit_time) - timedelta(hours=1)).time()
        end_window = (datetime.combine(date.today(), visit_req.visit_time) + timedelta(hours=1)).time()
        
        conflict = VisitRequest.objects.filter(
            property=visit_req.property,
            visit_date=visit_req.visit_date,
            status='approved',
            visit_time__range=(start_window, end_window)
        ).exclude(pk=visit_req.pk).exists()

        if conflict:
            messages.error(request, "Cannot approve: Conflict with another approved visit.")
            return redirect('properties:my_visit_requests')

        visit_req.status = 'approved'
        visit_req.save()
        
        send_mail(
            f"Visit Approved: {prop_title}",
            f"Your visit for {prop_title} on {visit_req.visit_date} at {visit_req.visit_time} is APPROVED.",
            settings.EMAIL_HOST_USER,
            [requester_email],
            fail_silently=True
        )
        messages.success(request, "Request approved.")

    elif action == 'reject':
        visit_req.status = 'rejected'
        visit_req.save()
        
        send_mail(
            f"Visit Rejected: {prop_title}",
            f"Sorry, your visit request for {prop_title} was rejected.",
            settings.EMAIL_HOST_USER,
            [requester_email],
            fail_silently=True
        )
        messages.warning(request, "Request rejected.")

    return redirect('properties:my_visit_requests')



def delete_visit_request(request, request_id):
    visit_req = get_object_or_404(VisitRequest, pk=request_id)
    
    if request.user == visit_req.requester or request.user == visit_req.property.owner:
        visit_req.delete()
        messages.success(request, "Visit request deleted.")
    else:
        messages.error(request, "You do not have permission to delete this request.")

    return redirect('properties:my_visit_requests')
