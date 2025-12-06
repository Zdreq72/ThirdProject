from django.db import models
from django.conf import settings
from properties.models import Property

class Inquiry(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inquiries')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.sender} on {self.property}"


    

    
class InquiryReply(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name="replies")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(null=False, blank=False)   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.sender}"