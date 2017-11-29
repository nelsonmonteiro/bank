from django.conf.urls import url
from ..views.api import *


urlpatterns = [
    url(r'^$', LoanView.as_view()),
    url(r'^(?P<pk>\d+)/balance/$', LoanBalanceView.as_view()),
    url(r'^(?P<pk>\d+)/payments/$', PaymentView.as_view()),
]
