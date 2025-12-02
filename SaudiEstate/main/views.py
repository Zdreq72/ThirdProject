from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')


def all_properties(request):
    return render(request, 'main/all_properties.html')
