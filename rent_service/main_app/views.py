from django.http import HttpResponse
from django.shortcuts import render
from .tasks import task_one, generate_recurring_payments

# Create your views here.
def test(request):
    generate_recurring_payments.delay()
    return HttpResponse("Hello, this is a response.")
