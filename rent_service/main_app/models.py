from django.db import models
from datetime import timedelta

class RentPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.IntegerField()
    property = models.IntegerField() 
    payment_date = models.DateField()
    is_recurring = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)


class RentalAgreement(models.Model):
    user = models.IntegerField()
    property = models.IntegerField() 
    start_date = models.DateField()
    last_payment_date = models.DateField(null=True, blank=True)
    is_on_rent = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
            # If last_payment_date is not provided, set it to three days after start_date
            if not self.last_payment_date:
                self.last_payment_date = self.start_date + timedelta(days=3)
            super().save(*args, **kwargs)


class MonthlyPayment(models.Model):
    rental_agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    
