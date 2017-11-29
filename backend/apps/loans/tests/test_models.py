import datetime
from django.test import TestCase
from django.utils.timezone import utc
from ..models import Payment, Loan


class LoanModelsTestCase(TestCase):
    def setUp(self):
        Loan.objects.create(
            amount=1000, term=12, rate=0.05,
            date=datetime.datetime(2017, 8, 5, 2, 18, tzinfo=utc)
        )

    def test_initial_data_of_a_loan(self):
        loan_1 = Loan.objects.earliest('id')
        self.assertEquals(loan_1.amount, 1000)
        self.assertEquals(loan_1.term, 12)
        self.assertEquals(loan_1.rate, 0.05)
        self.assertEquals(loan_1.date, datetime.datetime(2017, 8, 5, 2, 18, tzinfo=utc))
        self.assertEquals(loan_1.installment, 85.61)
        self.assertEquals(loan_1.amount_with_interest, 1027.32)
        self.assertEquals(loan_1.balance, 1027.32)

    def test_payments(self):
        loan_1 = Loan.objects.earliest('id')
        date = loan_1.date

        # Paying 11 months should be missing only an installment on the balance
        for _ in range(0, 11):
            date += datetime.timedelta(days=31)
            loan_1.payments.create(amount=loan_1.installment, date=date, payment=Payment.STATUS_TYPES.MADE)
        self.assertEquals(loan_1.balance, 85.61)

        # Missing a month keep balance the same
        date += datetime.timedelta(days=31)
        loan_1.payments.create(amount=loan_1.installment, date=date, payment=Payment.STATUS_TYPES.MISSED)
        self.assertEquals(loan_1.balance, 85.61)

        # Paying the last month that was missing should put the balance on 0
        payment = Payment.objects.latest('id')
        payment.payment = Payment.STATUS_TYPES.MADE
        payment.save()
        loan_1 = Loan.objects.earliest('id')
        self.assertEquals(loan_1.balance, 0)
