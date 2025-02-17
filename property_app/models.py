from django.db import models
from django.utils import timezone
from PIL import Image
from django.contrib.auth import get_user_model

# Define ROLE_CHOICES
ROLE_CHOICES = [
    ('tenant', 'Tenant'),
    ('owner', 'Owner'),
]

# (Removed module-level helper function to prevent potential DB access during initialization)

class Property(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('pending', 'Pending'),
    ]
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('pg', 'PG'),
        ('land', 'Land'),
        ('hotel', 'Hotel'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='apartment')
    amenities = models.ManyToManyField('Amenity')
    images = models.ManyToManyField('PropertyImage', related_name='properties')
    video = models.FileField(upload_to='property_videos/', null=True, blank=True)
    url = models.URLField(max_length=200, default='http://example.com')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    contact_name = models.CharField(max_length=100, default='Default Name')
    contact_email = models.EmailField(default='default@example.com')
    contact_phone = models.CharField(max_length=15, default='000-000-0000')
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title

class Amenity(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_images')
    image = models.ImageField(upload_to='properties/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 800 or img.width > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.image.url

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.property.title}'

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')
    saved_properties = models.ManyToManyField(Property, related_name='saved_by', blank=True)
    rental_history = models.ManyToManyField(Property, related_name='rented_by', blank=True)

    def __str__(self):
        return self.user.username

class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username}'

class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(get_user_model(), related_name='received_messages', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.recipient.username}'

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomUser(models.Model):
    phone_number = models.CharField(max_length=15)
    current_location = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profile_photos/')
    aadhar_number = models.CharField(max_length=12, blank=True)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('paytm', 'Paytm'),
        ('phonepe', 'PhonePe'),
        ('googlepay', 'Google Pay'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='razorpay')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f'Payment {self.id} - {self.method} - {self.status}'

class DocumentVerification(models.Model):
    DOCUMENT_TYPES = [
        ('aadhaar', 'Aadhaar Card'),
        ('pan', 'PAN Card'),
        ('license', 'Driving License'),
    ]
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_front = models.FileField(upload_to='verification/')
    document_back = models.FileField(upload_to='verification/', blank=True)
    is_verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.property.title} - {self.title}"
