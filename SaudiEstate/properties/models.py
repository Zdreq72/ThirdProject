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

    PROPERTY_PURPOSE_CHOICES = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    )

    PROPERTY_STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold'),
    )

    CITIES = [
       ('Riyadh', 'Riyadh'),
       ('Jeddah', 'Jeddah'),
       ('Dammam', 'Dammam'),
       ('Khobar', 'Khobar'),
       ('Makkah', 'Makkah'),
       ('Madina', 'Madina'),
       ('Abha', 'Abha'),
       ('Tabuk', 'Tabuk'),
       ('Qassim', 'Qassim'),
       ('Hail', 'Hail'),
       ('Najran', 'Najran'),
       ('Jazan', 'Jazan'),
       ('Buraidah', 'Buraidah'),
       ('Al-Ahsa', 'Al-Ahsa'),
       ('Taif', 'Taif'),
       ('Baha', 'Baha')
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=100, choices=CITIES)
    district = models.CharField(max_length=100)
    location = models.CharField(max_length=300, default='')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)

    purpose = models.CharField(max_length=10, choices=PROPERTY_PURPOSE_CHOICES, default='sale')
    status = models.CharField(max_length=10, choices=PROPERTY_STATUS_CHOICES, default='available')

    main_image = models.ImageField(upload_to='media/properties/main/')
    title_deed = models.FileField(upload_to='media/properties/documents/')
    ownership_proof = models.FileField(upload_to='media/properties/documents/')
    building_license = models.FileField(upload_to='media/properties/documents/', blank=True, null=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    deed_number = models.CharField(max_length=50, unique=True, null=True, blank=True)

    is_for_sale = models.BooleanField(default=True)

    def is_favorited_by(self, user):
        return self.favorited_by.filter(user=user).exists()

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/gallery/')

    def __str__(self):
        return f"Image for {self.property.title}"

class VisitRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visit_requests')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='visit_requests')
    visit_date = models.DateField()
    visit_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Visit for {self.property.title} by {self.requester.username}"





class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} → {self.property.title}"
