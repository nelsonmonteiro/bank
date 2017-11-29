import json
import datetime
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.utils.timezone import utc
from ..models import Loan, Payment


class LoanAPIViewsTestCase(APITestCase):
    def setUp(self):
        User.objects.create(username='user1', email='testuser1@djina.com')
        loan1 = Loan.objects.create(
            amount=1000, term=12, rate=0.05,
            date=datetime.datetime(2017, 8, 5, 2, 18, tzinfo=utc)
        )
        loan1.payments.create(amount=85.61, payment=Payment.STATUS_TYPES.MADE,
                              date=datetime.datetime(2017, 12, 5, 2, 18, tzinfo=utc))

        loan2 = Loan.objects.create(
            amount=1000, term=12, rate=0.05,
            date=datetime.datetime(2016, 8, 5, 2, 18, tzinfo=utc)
        )
        loan2.payments.create(amount=85.61, payment=Payment.STATUS_TYPES.MADE,
                              date=datetime.datetime(2016, 9, 5, 2, 18, tzinfo=utc))

    def test_create_loan(self):
        loan_data = json.dumps({
            'amount': 1000,
            'term': 12,
            'rate': 0.05,
            'date': '2017-08-05 02:18Z',
        })

        # --------------------------------------------------------------------------
        # Test authentication
        # --------------------------------------------------------------------------
        response = self.client.post('/api/loans/', data=loan_data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

        user1 = User.objects.earliest('id')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user1.auth_token.key)

        # --------------------------------------------------------------------------
        # Check if the loan creation is returning the right object
        # --------------------------------------------------------------------------
        response = self.client.post('/api/loans/', data=loan_data, content_type='application/json')
        new_loan = response.data
        self.assertEquals(response.status_code, 201)
        self.assertEquals(new_loan, {'loan_id': 3, 'installment': 85.61})

    def test_loans_list(self):
        # --------------------------------------------------------------------------
        # Test authentication
        # --------------------------------------------------------------------------
        response = self.client.get('/api/loans/', content_type='application/json')
        self.assertEqual(response.status_code, 403)

        user1 = User.objects.earliest('id')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user1.auth_token.key)

        # --------------------------------------------------------------------------
        # Test if the list is returning the right objects
        # --------------------------------------------------------------------------
        response = self.client.get('/api/loans/', content_type='application/json')
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 2)
        loan = data['results'][0]
        self.assertEqual(loan['id'], 1)
        self.assertEqual(loan['amount'], 1000)
        self.assertEqual(loan['term'], 12)
        self.assertEqual(loan['rate'], 0.05)
        self.assertEqual(loan['installment'], 85.61)
        self.assertEqual(loan['balance'], 941.71)

        # Add another loan
        self.client.post('/api/loans/', data=json.dumps({
            'amount': 1000,
            'term': 12,
            'rate': 0.05,
            'date': '2017-08-05 02:18Z',
        }), content_type='application/json')

        response = self.client.get('/api/loans/', content_type='application/json')
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 3)

    def test_loan_balance(self):
        # --------------------------------------------------------------------------
        # Test authentication
        # --------------------------------------------------------------------------
        response = self.client.post('/api/loans/1/balance/', content_type='application/json')
        self.assertEqual(response.status_code, 403)

        user1 = User.objects.earliest('id')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user1.auth_token.key)

        # --------------------------------------------------------------------------
        # Check current balance or for a specific date
        # --------------------------------------------------------------------------

        # Object doesn't exist
        response = self.client.post('/api/loans/20/balance/', content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # Current Balance
        response = self.client.post('/api/loans/1/balance/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'balance': 941.71})

        # Invalid date: Return current balance
        invalid_date = json.dumps({'date': 'asdsa'})
        response = self.client.post('/api/loans/1/balance/', data=invalid_date, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'balance': 941.71})

        # Valid date: Return the balance at that date
        valid_date = json.dumps({'date': '2017-10-05 02:18Z'})
        response = self.client.post('/api/loans/1/balance/', data=valid_date, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'balance': 1027.32})

    def test_create_payment(self):
        url = '/api/loans/2/payments/'
        date = datetime.datetime(2016, 9, 1, 20, 30, tzinfo=utc)

        missed_payment_data = {
            'amount': 85.61,
            'payment': Payment.STATUS_TYPES.MISSED,
            'date': date.isoformat()
        }

        payment_data = {
            'amount': 85.61,
            'payment': Payment.STATUS_TYPES.MADE,
            'date': date.isoformat()
        }

        # --------------------------------------------------------------------------
        # Test authentication
        # --------------------------------------------------------------------------
        response = self.client.post(url, data=json.dumps(payment_data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

        user1 = User.objects.earliest('id')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user1.auth_token.key)

        # --------------------------------------------------------------------------
        # SHOULD FAIL: There's a payment already for this month
        # --------------------------------------------------------------------------
        response = self.client.post(url, data=json.dumps(missed_payment_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url, data=json.dumps(payment_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        date += datetime.timedelta(days=31)
        missed_payment_data['date'] = date.isoformat()
        payment_data['date'] = date.isoformat()

        # --------------------------------------------------------------------------
        # Create a missing payment and replace with a paid one
        # --------------------------------------------------------------------------
        response = self.client.post(url, data=json.dumps(missed_payment_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/api/loans/2/balance/', content_type='application/json')
        self.assertEqual(response.data, {'balance': 941.71})

        response = self.client.post(url, data=json.dumps(payment_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/api/loans/2/balance/', content_type='application/json')
        self.assertEqual(response.data, {'balance': 856.1})

        # --------------------------------------------------------------------------
        # The rest of the payments should be done without any problems
        # --------------------------------------------------------------------------
        for _ in range(0, 10):
            date += datetime.timedelta(days=31)
            payment_data['date'] = date.isoformat()
            response = self.client.post(url, data=json.dumps(payment_data), content_type='application/json')
            self.assertEqual(response.status_code, 201)

        # --------------------------------------------------------------------------
        # THIS SHOULD FAIL: The loan has been payed at this moment
        # --------------------------------------------------------------------------
        date += datetime.timedelta(days=31)
        payment_data['date'] = date.isoformat()
        response = self.client.post(url, data=json.dumps(payment_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_payments_list(self):
        # --------------------------------------------------------------------------
        # Test authentication
        # --------------------------------------------------------------------------
        response = self.client.get('/api/loans/1/payments/', content_type='application/json')
        self.assertEqual(response.status_code, 403)

        user1 = User.objects.earliest('id')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user1.auth_token.key)

        # --------------------------------------------------------------------------
        # Test if the list is returning the right objects
        # --------------------------------------------------------------------------

        # Object doesn't exist
        response = self.client.get('/api/loans/20/payments/', content_type='application/json')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/api/loans/1/payments/', content_type='application/json')
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 1)


