# James: Software Engineer Challenge

The objective of this challenge is to test your ability to implement a solution upon given an abstract problem.

We want you to develop an application through which a big bank can easily issue new loans and find out what the value and volume of outstanding debt are.

<b>Problem:</b>
- A big bank needs to keep track of the amount of money loaned out and the missed/made payments.
- A big bank needs a place to retrieve the volume of outstanding debt at some point in time.

<b>Limitations:</b>
- Loans are paid back in monthly installments.

## Requirements
- Python 2.7 or Python 3
- pip & virtualenv


## Installation

#### Clone project from GitHub
```
git clone https://github.com/nelsonmonteiro/bank.git
```

#### Setup project locally
```
cd bank/
./setup
```
Follow the steps that will appear on your console to create a superuser when installation is complete.

#### Run server
```
./runserver
```
The server will be running on http://127.0.0.1:8000/


## API Endpoints

### API TOKEN
For security reasons, you will need an Authorization token to make your API calls. You can also use your session if you are making your calls from a browser.

The token key should be included in the Authorization HTTP header. The key should be prefixed by the string literal "Token", with whitespace separating the two strings. For example:

Authorization: Token fd5104f5741bc8ca17e33f27c0f8f9982ac6bffb

To access to your token, login at http://127.0.0.1:8000/ after setting up the project locally and have created a superuser.


### GET /api/loans

#### Summary

Return the list of all loans.

#### Reply

- id: unique id of the loan.
- installment: monthly loan payment.
- term: number of months that will take until its gets paid-off.
- rate: interest rate as decimal.
- date: when a loan was asked (origination date as an ISO 8601 string).

###### Example

```
{
    "count": 20,
    "next": "/api/loans/?page=1",
    "previous" "/api/loans/?page=3",
    "results": [
        {
            "id": 56,
            "amount": 1000,
            "term": 12,
            "rate": 0.05,
            "date": "2017-08-05 02:18Z",
        },
        ...
    ]
}
```

### POST /api/loans

#### Summary

Creates a loan application. Loans are automatically accepted.

#### Payload
- amount: loan amount in dollars.
- term: number of months that will take until its gets paid-off.
- rate: interest rate as decimal.
- date: when a loan was asked (origination date as an ISO 8601 string).

###### Example
```
{
	"amount": 1000,
	"term": 12,
	"rate": 0.05,
	"date": "2017-08-05 02:18Z",
}
```

#### Reply

- loan_id: unique id of the loan.
- installment: monthly loan payment.

###### Example

```
{
	"loan_id": 305,
	"installment": 85.60
}
```

### POST /api/loans/<:id>/payments

#### Summary

Creates a record of a payment `made` or `missed`.

#### Payload

- payment: type of payment: `made` or `missed`.
- date: payment date.
- amount: amount of the payment `made` or `missed` in dollars.

###### Example (Payment made)
```
{
  "payment": "made",
  "date": "2017-09-05 02:18Z",
  "amount": 85.60,
}
```
###### Example (Payment missed)
```
{
  "payment": "missed",
  "date": "2017-09-05 02:18Z",
  "amount": 85.60,
}
```

### POST /api/loans/<:id>/balance

#### Summary

Get the volume of outstanding debt (i.e., debt yet to be paid) at some point in time.

#### Payload

- date: loan balance until this date. (Optional)

###### Example
```
{
  "date": "2017-09-05 02:18Z"
}
```

#### Reply

- balance: outstanding debt of loan.

###### Example
```
{
	"balance": 40
}
```
