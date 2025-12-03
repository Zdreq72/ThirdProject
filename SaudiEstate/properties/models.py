from django.db import models
from django.conf import settings

class Property(models.Model):
    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    PROPERTY_TYPE_CHOICES = (
        ('villa', 'Villa'),
        ('apartment', 'Apartment'),
        ('land', 'Land'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    location = models.CharField(max_length=300, default='')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    main_image = models.ImageField(upload_to='media/properties/main/')
    title_deed = models.FileField(upload_to='media/properties/documents/')
    ownership_proof = models.FileField(upload_to='media/properties/documents/')
    building_license = models.FileField(upload_to='media/properties/documents/', blank=True, null=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/gallery/')

    def __str__(self):
        return f"Image for {self.property.title}"