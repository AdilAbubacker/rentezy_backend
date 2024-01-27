from django.shortcuts import render
from main_app.models import MonthlyPayment, RentalAgreement
from rest_framework.views import APIView
from main_app.serializers import MonthlyPaymentSerializer, RentalAgreementSerializer
from rest_framework.response import Response
from rest_framework import status 

# Create your views here.
class RentedPropertiesListView(APIView):
    def get(self, request):
        bookings = RentalAgreement.objects.all()
        serializer = RentalAgreementSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RentPaymentDeatailsView(APIView):
    def get(self, request, rent_id):
        agreement = RentalAgreement.objects.get(id=rent_id)
        payments = MonthlyPayment.objects.filter(rental_agreement=agreement)
          
        # Serialize RentalAgreement along with MonthlyPayments
        agreement_serializer = RentalAgreementSerializer(agreement)
        payments_serializer = MonthlyPaymentSerializer(payments, many=True)

        # Combine the serialized data
        data = {
            'rental_agreement': agreement_serializer.data,
            'monthly_payments': payments_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    