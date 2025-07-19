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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
