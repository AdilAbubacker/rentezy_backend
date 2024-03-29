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
    property_name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
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

    def get_latest_monthly_payment(self):
            # Retrieve the latest MonthlyPayment associated with this RentalAgreement
            latest_payment = self.monthlypayment_set.order_by('-due_date').first()
            return latest_payment


class MonthlyPayment(models.Model):
    rental_agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    paid_on = models.DateField(null=True, blank=True)
    
