import datetime
from decimal import Decimal
from rent_service.celery import app
from celery import shared_task
from datetime import timezone, datetime
from .models import MonthlyPayment, RentPayment, RentalAgreement
from dateutil.relativedelta import relativedelta
from .kafka_producers import kafka_producer
from django.conf import settings
from datetime import datetime, timezone, timedelta


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
    today = datetime.now(timezone.utc).date()
    three_days_after = today + timedelta(days=3)
    three_days_before = today - timedelta(days=3)
    print(today, three_days_after, three_days_before)

    for payment in unpaid_payments:
        print(today, three_days_after, three_days_before)
        print(payment.rental_agreement.user,'userid')
        
        if payment.payment_date < three_days_before:
            # calculate late fee of 2% of rent for each day for nonpayment after due date
            late_fee_percentage = 0.02

            # Assuming late_fee_percentage is a float, convert it to Decimal
            late_fee_percentage_decimal = Decimal(str(late_fee_percentage))

            # Calculate late fee using Decimal multiplication
            late_fee = payment.amount * late_fee_percentage_decimal   
                         
            # Update payment amount with late fees
            payment.fine += late_fee
            payment.save()
            
            user_id = payment.rental_agreement.user
            print(user_id)
            message_content = 'helllooooo'

            # Send a reminder to the user
            message_template = '{"user_id":"{}","message":"{}"}'
            message = message_template.format(user_id, message_content)      
            print(f'{message:{message}}')
            kafka_producer.produce_message(message=message, topic=settings.KAFKA_NOTIFICATIONS_TOPIC)
        elif payment.payment_date == three_days_after:
            print('kkkkkkkkkkkkkkkkkkk')
                

@app.task
def task_one():
    message = '{"user_id":"3","message":"hello kkkkk"}'
    return "success"

@app.task
def task_two(data, *args, **kwargs):
    print(f" task two called with the argument {data} and worker is running good")
    return "success"