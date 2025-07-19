
from django.contrib.auth.models import AbstractUser
from django.db import models

class AppUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('attender', 'Attender'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attender')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)


    def __str__(self):
        return f"{self.username} ({self.role})"
