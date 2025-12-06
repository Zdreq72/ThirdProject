from django.urls import path
from . import views

app_name = "inquiries"

urlpatterns = [
    path("send/<int:pk>/", views.send_inquiry, name="send"),
    path("reply/<int:inquiry_id>/", views.reply_inquiry, name="reply"),
    path("delete/<int:inquiry_id>/", views.delete_inquiry, name="delete_inquiry"),
    path("delete_reply/<int:reply_id>/", views.delete_reply, name="delete_reply"),

]
