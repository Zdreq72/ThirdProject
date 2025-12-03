from django.shortcuts import render
from properties.models import Property

def home(request):    
    properties = Property.objects.all().order_by('?')

    
    
    if request.user.is_authenticated:
       
        user_city = getattr(request.user, 'city', None)
        
        if user_city:
            city_properties = Property.objects.filter(city__icontains=user_city).order_by('-created_at')
            if city_properties.exists():
                properties = city_properties
    featured_properties = properties[:3]

    context = {
        'properties': featured_properties
    }
    return render(request, 'main/home.html', context)


def all_properties(request):
    return render(request, 'main/all_properties.html')
