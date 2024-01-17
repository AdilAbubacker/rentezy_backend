from rest_framework import serializers
from .models import RentalAgreement, MonthlyPayment


class MonthlyPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyPayment
        fields = '__all__'


class RentalAgreementSerializer(serializers.ModelSerializer):
    latest_monthly_payment = MonthlyPaymentSerializer(read_only=True)

    class Meta:
        model = RentalAgreement
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        latest_monthly_payment = instance.get_latest_monthly_payment()

        # Include latest_monthly_payment data in the serialized representation
        if latest_monthly_payment:
            data['latest_monthly_payment'] = MonthlyPaymentSerializer(latest_monthly_payment).data
        else:
            data['latest_monthly_payment'] = None

        return data
