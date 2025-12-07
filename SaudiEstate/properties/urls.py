from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('<int:pk>/', views.property_detail, name='detail'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/remove/<int:fav_id>/', views.remove_favorite, name='remove_favorite'),
    path('add/', views.add_property, name='add_property'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('verify/<int:pk>/<str:action>/', views.verify_property, name='verify_property'),
    path('all/', views.all_properties, name='all_properties'),
    path('<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('<int:pk>/book-visit/', views.book_visit, name='book_visit'),
    path('visits/', views.my_visit_requests, name='my_visit_requests'),
    path('visits/handle/<int:request_id>/<str:action>/', views.handle_visit_request, name='handle_visit_request'),
    path('visits/delete/<int:request_id>/', views.delete_visit_request, name='delete_visit_request'),
]