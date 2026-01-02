from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q, F

# Create your models here.
class AvailableRooms(models.Model):
    room_id = models.IntegerField()
    property_name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    price = models.IntegerField()
    initial_quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField()
    
    class Meta:
        app_label = 'main_app'
        constraints = [
            models.CheckConstraint(
                check=Q(available_quantity__gte=0) & Q(available_quantity__lte=F('initial_quantity')),
                name="available_quantity_non_negative"
            )
        ]
        
    
class Booking(models.Model):
    STATUS = [
        ('reserved', 'Reserved'),
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    room_id = models.IntegerField()
    # room = models.ForeignKey(AvailableRooms, on_delete=models.SET_NULL, null=True, related_name='bookings')
    tenant_id = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS, default='reserved')
    move_in_date = models.DateField()
    no_of_rooms = models.IntegerField(default=1)

    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)
    
    idempotency_key = models.CharField(max_length=255, unique=True)
    celery_task_id = models.CharField(max_length=255, blank=True, null=True)

    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lease_agreement = models.FileField(upload_to='lease_agreements/', blank=True, null=True)

    stripe_session_url = models.CharField(max_length=255, blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'main_app'
        indexes = [
            models.Index(fields=['status', 'expires_at']),
            models.Index(fields=['stripe_session_id']),
        ]

        
        