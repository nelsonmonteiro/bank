from rest_framework import serializers
from .models import Loan, Payment


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'amount', 'rate', 'term', 'date', 'installment', 'balance']
        read_only_fields = ['balance']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment', 'amount', 'date']

    def validate(self, data):
        loan = self.context['loan']
        date = data['date']
        amount = data['amount']

        # check if the amount is equal to installment
        if loan.installment != amount:
            raise serializers.ValidationError('Payment amount differ from loan installment.')

        # check if balance is inferior of installment,
        # on this solution means that everything have been payed
        if loan.balance < amount:
            raise serializers.ValidationError('This loan has been paid already.')

        # check if exist already a payment for this month
        # if it exist but haven't been paid yet, it can be replaced by a paid one.
        payment_from_same_month = loan.payments.filter(date__year=date.year, date__month=date.month)
        if payment_from_same_month:
            current = payment_from_same_month[0]
            if data['payment'] == Payment.STATUS_TYPES.MADE and current.payment == Payment.STATUS_TYPES.MISSED:
                current.delete()
            else:
                raise serializers.ValidationError('A payment have been made already for this account.')

        data['loan_id'] = loan.id
        return data
