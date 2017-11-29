from django.contrib import admin
from .models import Payment, Loan


class PaymentChild(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'rate', 'term', 'installment', 'balance', 'date']
    inlines = [PaymentChild]
