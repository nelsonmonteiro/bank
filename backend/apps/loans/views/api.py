from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import dateparse
from ..serializers import LoanSerializer, PaymentSerializer
from ..models import Loan, Payment
from ..mixins import LoanChildViewMixin


# -----------------------------------------------------------------------------
# LOANS
# -----------------------------------------------------------------------------
class LoanView(ListAPIView, CreateAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def create(self, request, *args, **kwargs):
        # default behavior from rest_framework
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # clean return to match challenge
        return Response({
            'loan_id': serializer.instance.id,
            'installment': serializer.instance.installment,
        }, status=status.HTTP_201_CREATED, headers=headers)


class LoanBalanceView(CreateAPIView):
    """
    Return the balance of a loan.
    If the date is empty or invalid, returns the current balance.
    """
    queryset = Loan.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        date = dateparse.parse_datetime(request.data.get('date', ''))
        return Response({'balance': instance.calculate_balance(date=date)})


# -----------------------------------------------------------------------------
# PAYMENTS
# -----------------------------------------------------------------------------
class PaymentView(LoanChildViewMixin, ListAPIView, CreateAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return self.get_loan().payments.all()

    def get_serializer_context(self):
        context = super(PaymentView, self).get_serializer_context()
        context['loan'] = self.get_loan()
        return context
