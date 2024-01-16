import datetime
from decimal import Decimal
import json
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
    seven_days_after = today + timedelta(days=7)

    for payment in unpaid_payments:
        user_id = payment.rental_agreement.user
        # Extracting the month from the payment date
        month_name = payment.payment_date.strftime("%B")

        if payment.payment_date < today:
            payment.fine += 100
            payment.save()

            subject = 'Overdue Rent Payment with Daily Late Fee'
            message_content =  f'🚨🚨🚨 Alert!!: Your monthly rent for PropertyId:{payment.rental_agreement.property} for {month_name} is overdue and remains unpaid. Daily late fee of 100 Rupees is being incurred. Please settle immediately to avoid additional charges.'

            # Send a reminder to the user
            message_data = {"user_id": user_id, "message": message_content}

            # Convert dictionary to JSON string for sending through kafka
            message_json = json.dumps(message_data)
            print(message_json)    

            # Send data to notification service through kafka
            kafka_producer.produce_message(message=message_json, topic=settings.KAFKA_NOTIFICATIONS_TOPIC)

        elif payment.payment_date == today:
            subject = 'Overdue Rent Payment with Daily Late Fee'
            print(user_id)
            message_content = f"🚨 Reminder: Last date for your rent payment for PropertyId:{payment.rental_agreement.property} for the month {month_name} is today. Please ensure to make the payment by the end of the day to avoid late fees of 100 per day. 🏡💸"
           
            # Send a reminder to the user
            message_data = {"user_id": user_id, "message": message_content}

            # Convert dictionary to JSON string for sending through kafka
            message_json = json.dumps(message_data)
            print(message_json)    

            # Send data to notification service through kafka
            kafka_producer.produce_message(message=message_json, topic=settings.KAFKA_NOTIFICATIONS_TOPIC)

        elif payment.payment_date == three_days_after:
            message_content = f"🚨 Reminder: Your rent payment for PropertyId:{payment.rental_agreement.property} is due in 3 days, {three_days_after.strftime('%B %d')}. Please ensure to make the payment on time to avoid any late fees. 🏡💸"

            # Send a reminder to the user
            message_data = {"user_id": user_id, "message": message_content}
            message_json = json.dumps(message_data)
            print(message_json)    

            # Send data to notification service through kafka
            kafka_producer.produce_message(message=message_json, topic=settings.KAFKA_NOTIFICATIONS_TOPIC)

        elif payment.payment_date == seven_days_after:
            message_content = f"🚨 Reminder: Your rent payment for PropertyId:{payment.rental_agreement.property} is due in 7 days on {seven_days_after.strftime('%B %d')}. Please plan accordingly. 🏡💸"

            # Send a reminder to the user
            message_data = {"user_id": user_id, "message": message_content}

            # Convert dictionary to JSON string for sending through kafka
            message_json = json.dumps(message_data)
            print(message_json)    

            # Send data to notification service through kafka
            kafka_producer.produce_message(message=message_json, topic=settings.KAFKA_NOTIFICATIONS_TOPIC)

                

@app.task
def task_one():
    message = '{"user_id":"3","message":"hello kkkkk"}'
    return "success"

@app.task
def task_two(data, *args, **kwargs):
    print(f" task two called with the argument {data} and worker is running good")
    return "success"