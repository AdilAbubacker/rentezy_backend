from django.http import HttpResponse
from django.shortcuts import render
from .tasks import send_rent_reminders, task_one, generate_recurring_payments
from .kafka_producers import kafka_producer
from django.conf import settings

# Create your views here.
def test(request):
    # generate_recurring_payments.delay()
    message = '{"user_id":"3","message":"hpw adfri"}'
    print(message)
    send_rent_reminders.delay()
    # kafka_producer.produce_message(message=message,topic=settings.KAFKA_NOTIFICATIONS_TOPIC)
    return HttpResponse("Hello, this is a response.")
