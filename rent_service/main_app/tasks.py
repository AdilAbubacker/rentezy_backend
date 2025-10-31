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
    """
    Generate all missing monthly payment records for active rental agreements.
    This task is idempotent and self-healing - it will catch up on any missed payments.
    """
    rental_agreements = RentalAgreement.objects.filter(is_on_rent=True)
    today = datetime.now().date()

    for rental_agreement in rental_agreements:
        # Skip if the rental agreement hasn't started yet
        if rental_agreement.start_date > today:
            continue

        # Calculate the next payment date
        next_payment_date = (
            rental_agreement.last_payment_date + relativedelta(months=1)
            if rental_agreement.last_payment_date
            else rental_agreement.start_date
        )

        # Generate ALL missing payments up to today (self-healing loop)
        while next_payment_date <= today:
            _, created = MonthlyPayment.objects.get_or_create(
                rental_agreement=rental_agreement,
                due_date=next_payment_date,
                defaults={"amount": rental_agreement.amount}
            )
            
            # Only update last_payment_date if a new payment was actually created
            if created:
                rental_agreement.last_payment_date = next_payment_date
                rental_agreement.save(update_fields=['last_payment_date'])
            
            next_payment_date += relativedelta(months=1)

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
        month_name = payment.due_date.strftime("%B")

        if payment.due_date < today:
            # Idempotent Fine Calculation: Formula based (Days Overdue * 100)
            days_overdue = (today - payment.due_date).days
            new_fine = days_overdue * 100
            
            if payment.fine != new_fine:
                payment.fine = new_fine
                payment.save(update_fields=['fine'])

            subject = 'Overdue Rent Payment with Daily Late Fee'
            message_content =  f'🚨🚨🚨 Alert!!: Your monthly rent for PropertyId:{payment.rental_agreement.property} for {month_name} is overdue and remains unpaid. Daily late fee of 100 Rupees is being incurred. Please settle immediately to avoid additional charges.' 

            send_notification_through_kafka(user_id, message_content)

        elif payment.due_date == today:
            message_content = f"🚨 Reminder: Last date for your rent payment for PropertyId:{payment.rental_agreement.property} for the month {month_name} is today. Please ensure to make the payment by the end of the day to avoid late fees of 100 per day. 🏡💸"
    
            # Send data to notification service through kafka
            send_notification_through_kafka(user_id, message_content)

        elif payment.due_date == three_days_after:
            message_content = f"🚨 Reminder: Your rent payment for PropertyId:{payment.rental_agreement.property} is due in 3 days, {three_days_after.strftime('%B %d')}. Please ensure to make the payment on time to avoid any late fees. 🏡💸"

            # Send data to notification service through kafka
            send_notification_through_kafka(user_id, message_content)

        elif payment.due_date == seven_days_after:
            message_content = f"🚨 Reminder: Your rent payment for PropertyId:{payment.rental_agreement.property} is due in 7 days on {seven_days_after.strftime('%B %d')}. Please plan accordingly. 🏡💸"

            # Send data to notification service through kafka
            send_notification_through_kafka(user_id, message_content)


def send_notification_through_kafka(user_id, message_content):
    # Create dictionary for kafka
    message_data = {"user_id": user_id, "message": message_content}

    # Convert dictionary to JSON string for sending through kafka
    message_json = json.dumps(message_data)

    # send content to the notifications kafka topic
    kafka_producer.produce_message(message=message_json, topic=settings.KAFKA_NOTIFICATIONS_TOPIC)


@app.task
def task_one():
    message = '{"user_id":"3","message":"hello kkkkk"}'
    return "success"

@app.task
def task_two(data, *args, **kwargs):
    print(f" task two called with the argument {data} and worker is running good")
    return "success"