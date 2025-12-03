from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('all-properties/', views.all_properties, name='all_properties'),
    path('about/', views.about, name='about'),
    


]