import math
from django.db import models
from django.db.models import Sum
from django.utils.encoding import python_2_unicode_compatible
from apps.core.utils.models import BaseModel, get_namedtuple_choices


@python_2_unicode_compatible
class Loan(BaseModel):
    class Meta:
        ordering = ['-date']

    amount = models.FloatField()
    rate = models.FloatField()
    term = models.PositiveSmallIntegerField()
    date = models.DateTimeField()

    # cached data
    balance = models.FloatField()

    @property
    def installment(self):
        r = self.rate / 12.
        return round((r + r / (math.pow((1 + r), self.term) - 1)) * self.amount, 2)

    @property
    def amount_with_interest(self):
        return round(self.installment * self.term, 2)

    def calculate_balance(self, date=None):
        queryset = self.payments.filter(payment=Payment.STATUS_TYPES.MADE)
        if date:
            queryset = queryset.filter(date__lte=date)

        total_payments = queryset.aggregate(
            total_payments=Sum('amount')).get('total_payments') or 0
        return round(self.amount_with_interest - total_payments, 2)

    def update_balance(self, commit=True):
        self.balance = self.calculate_balance()
        if commit:
            super(Loan, self).save()

    def save(self, *args, **kwargs):
        self.update_balance(commit=False)
        super(Loan, self).save(*args, **kwargs)

    def __str__(self):
        return 'Loan %s: %s' % (self.id, self.amount)


@python_2_unicode_compatible
class Payment(BaseModel):
    class Meta:
        ordering = ['-date']

    STATUS_TYPES = get_namedtuple_choices('LOANS_PAYMENTS_STATUS_TYPES', (
        ('made', 'MADE', 'Payment as been made'),
        ('missed', 'MISSED', 'Missed payment'),
    ))

    loan = models.ForeignKey(Loan, related_name='payments')
    payment = models.CharField(max_length=6, choices=STATUS_TYPES.get_choices())
    amount = models.FloatField()
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        super(Payment, self).save(*args, **kwargs)
        self.loan.update_balance()

    def delete(self, *args, **kwargs):
        loan = self.loan
        super(Payment, self).delete(*args, **kwargs)
        loan.update_balance()

    def __str__(self):
        return 'Payment %s: %s (%s)' % (self.id, self.amount, self.get_payment_display())
