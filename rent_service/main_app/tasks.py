import datetime
from rent_service.celery import app
from celery import shared_task
from datetime import timedelta, timezone
from datetime import datetime
from .models import MonthlyPayment, RentPayment, RentalAgreement
from dateutil.relativedelta import relativedelta


@app.task
def generate_recurring_payments():
    rental_agreements = RentalAgreement.objects.filter(is_on_rent=True)
    today = datetime.now().date()

    for rental_agreement in rental_agreements:
        print(rental_agreement.id)

        # Check if the rental agreement is active
        if rental_agreement.start_date > today:
            continue

        # Calculate the next payment date using relativedelta for accurate monthly intervals
        next_payment_date = rental_agreement.last_payment_date + relativedelta(months=1) if rental_agreement.last_payment_date else rental_agreement.start_date

        # Create a new monthly payment instance
        new_payment = MonthlyPayment(
            rental_agreement=rental_agreement,
            payment_date=next_payment_date,
            amount=rental_agreement.amount 
        )
        new_payment.save()

        # Update the last payment date in the rental agreement model
        rental_agreement.last_payment_date = next_payment_date
        rental_agreement.save()

    return 'success'


@app.task
def send_rent_reminders():
    unpaid_payments = MonthlyPayment.objects.filter(is_paid=False)
    
    for payment in unpaid_payments:
        today = timezone.now().date()
        three_days_after = today + timezone.timedelta(days=3)
        three_days_before = today - timezone.timedelta(days=3)
        print(today, three_days_after, three_days_before)

        if payment.payment_date < three_days_before:
            # calculate late fee of 2% of rent for each day for nonpayment after due date
            late_fee_percentage = 0.02

            late_fee = payment.amount * late_fee_percentage
                
            # Update payment amount with late fees
            payment.amount_payable += late_fee
            payment.save()
                
            # Send a reminder to the user
            # send_overdue_payment_reminder(payment.user, payment.due_date, late_fee)

        elif payment.payment_date == three_days_before:
            pass
                

@app.task
def task_one():
    for i in range(10):
        print(i)
    print(" task one called and worker is running good")
    return "success"

@app.task
def task_two(data, *args, **kwargs):
    print(f" task two called with the argument {data} and worker is running good")
    return "success"