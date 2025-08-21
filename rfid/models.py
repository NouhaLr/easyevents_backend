
from django.db import models
from django.utils import timezone

class Bracelet(models.Model):
    """
    Links a (fake) RFID tag UID to a Reservation.
    One bracelet per reservation in this first version.
    """
    reservation = models.OneToOneField(
        'events.Reservation',
        on_delete=models.CASCADE,
        related_name='bracelet'
    )
    tag_uid = models.CharField(max_length=128, unique=True)
    active = models.BooleanField(default=True)
    issued_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tag_uid} -> {self.reservation.receipt_number}"
