from rest_framework.exceptions import NotFound
from .models import Loan


class LoanChildViewMixin(object):
    """
    Helps to get the Loan instance from url
    """

    def get_loan(self):
        if not hasattr(self, 'loan'):
            try:
                self.loan = Loan.objects.prefetch_related('payments').get(pk=self.kwargs.get('pk'))
            except Loan.DoesNotExist:
                raise NotFound('Loan object not found.')
        return self.loan