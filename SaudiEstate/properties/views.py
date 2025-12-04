from django.shortcuts import render, get_object_or_404 , redirect
from .models import Property
from django.db.models import Q
from django.contrib import messages




def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    related_properties = Property.objects.filter(
        Q(city=property.city) | 
        Q(property_type=property.property_type) |
        Q(price__range=(float(property.price) * 0.8, float(property.price) * 1.2))
    ).exclude(pk=pk).distinct().order_by('?')[:3] 

    context = {
        'property': property,
        'related_properties': related_properties
    }
    return render(request, 'properties/property.html', context)


def add_property(request):

    if request.method == 'POST':

        if not request.user.is_authenticated:
            messages.error(request, "Please login to add a property.")
            return redirect('users:login')

        try:
            new_property = Property(
                owner=request.user,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                city=request.POST.get('city'),
                district=request.POST.get('district'),
                location=request.POST.get('location'),
                price=request.POST.get('price'),
                area=request.POST.get('area'),
                rooms=request.POST.get('rooms'),
                bathrooms=request.POST.get('bathrooms'),
                age=request.POST.get('age'),
                property_type=request.POST.get('property_type'),
                
                main_image=request.FILES.get('main_image'),
                title_deed=request.FILES.get('title_deed'),
                ownership_proof=request.FILES.get('ownership_proof'),
                building_license=request.FILES.get('building_license')
            )
            new_property.save()
            messages.success(request, "Property submitted successfully! Pending approval.")
            return redirect('main:home')
            
        except Exception as e:
            print(e)
            messages.error(request, "Error adding property. Please check your inputs.")


    context = {
        'cities': Property.CITIES,
        'types': Property.PROPERTY_TYPE_CHOICES
    }
    return render(request, 'properties/add_property.html', context)