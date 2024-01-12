from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class AvailableRooms(models.Model):
    room_id = models.IntegerField()
    price = models.IntegerField()
    initial_quantity = models.IntegerField()
    available_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    
    
class Booking(models.Model):
    STATUS = [
        ('reserved', 'Reserved'),
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    room_id = models.IntegerField()
    tenant_id = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS, default='reserved')
    move_in_date = models.DateField()
    no_of_rooms = models.IntegerField(default=1)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lease_agreement = models.FileField(upload_to='lease_agreements/', blank=True, null=True)