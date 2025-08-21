from django.db import models

# Create your models here.
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    place = models.CharField(max_length=100)
    description = models.TextField(blank=True)  
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)  
    plan = models.TextField(blank=True)
    normal_ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    vip_ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    max_attendees = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
    
import uuid
from django.db import models
from django.conf import settings

# models.py
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    ticket_type = models.CharField(max_length=10, choices=[('normal', 'Normal'), ('vip', 'VIP')])
    quantity = models.PositiveIntegerField(default=1)  # NEW
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # NEW
    address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=[('card', 'Card'), ('reception', 'At Reception')])
    receipt_number = models.CharField(max_length=20, unique=True, editable=False, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.event.name}"
