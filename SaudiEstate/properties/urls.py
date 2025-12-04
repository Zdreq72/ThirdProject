from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('<int:pk>/', views.property_detail, name='detail'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/remove/<int:fav_id>/', views.remove_favorite, name='remove_favorite'),
    path('add/', views.add_property, name='add_property'),
]