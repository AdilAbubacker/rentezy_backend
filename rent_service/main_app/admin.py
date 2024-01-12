from django.contrib import admin
from .models import MonthlyPayment, RentalAgreement, RentPayment

# Register your models here.
admin.site.register(RentalAgreement)
admin.site.register(MonthlyPayment)
admin.site.register(RentPayment)
