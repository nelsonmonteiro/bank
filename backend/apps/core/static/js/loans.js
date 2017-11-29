(function(){
  'use strict';

  var loanTemplate = $('#loan-template').html();
  var loansContainer = $('#loans-container');
  var loansPage, activeLoan;

  var paymentTemplate = $('#payment-template').html();
  var paymentsContainer = $('#payments-container');

  function sendAlert(title, message) {
    $('#message-title').html(title);

    if (typeof(message) === 'string') {
      $('#message-text').html(message);
    } else if (typeof message === 'object') {
      var keys = Object.keys(message);

      if (keys.length > 1) {
        var new_message = '';
        for (var key in message) {
          if (message.hasOwnProperty(key)) {
            new_message += '<b>'+ key +': </b>'+ message[key] +'<br>';
          }
        }
        $('#message-text').html(new_message);
      } else {
        $('#message-text').html(message[keys[0]]);
      }
    }

    $('#messages-modal').modal('open');
  }

  function updateLoans(page) {
    loansPage = page || 1;

    $.get({
      url: '/api/loans/?page=' + loansPage,
      dataType: 'json',
      success: function (response) {
        var loans = response.results;

        if (loans.length) {
          loansContainer.html('');
          for (var i=0; i < loans.length; i++) {
            loansContainer.append(_.template(loanTemplate)(loans[i]));
            updateLoansActions();
          }
        } else {
          loansContainer.html('<tr><td colspan="8">No loans have been added yet!</td></tr>');
        }
      }
    });
  }

  function updateLoansActions() {
    $('.view-payments').click(function (e) {
      e.preventDefault();
      activeLoan = $(this).data('loan-id');

      $.get({
        url: '/api/loans/'+ activeLoan +'/payments/',
        dataType: 'json',
        success: function (response) {
          var payments = response.results;

          if (payments.length) {
            paymentsContainer.html('');
            for (var i=0; i < payments.length; i++) {
              paymentsContainer.append(_.template(paymentTemplate)(payments[i]));
            }
          } else {
            paymentsContainer.html('<tr><td colspan="4">No payments have been made yet!</td></tr>');
          }
          $('#payments-list-modal').modal('open');
        }
      });
    });

    $('.new-payment').click(function (e) {
      activeLoan = $(this).data('loan-id');
      $('#new-payment-modal').modal('open');
    });
  }

  $('#new-payment-btn').click(function(e) {
    e.preventDefault();
    $('#payments-list-modal').modal('close');
    $('#new-payment-modal').modal('open');
  });


  // Create new loan
  $('#create-new-loan-form').submit(function(e) {
    e.preventDefault();
    var data = getFormData(this);
    var formModal = $('#create-new-loan-modal');
    data.date = new Date().toISOString();

    $.ajax({
      url: '/api/loans/',
      method: 'post',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      success: function() {
        updateLoans();
        formModal.modal('close');
        formModal.find('input').val('');
      },
      error: function(jqXHR, textStatus, errorThrown) {
        sendAlert('Create new loan', jqXHR.responseJSON.detail);
      }
    });
  });

  // Create new payment
  $('#create-new-payment-form').submit(function(e) {
    e.preventDefault();
    var data = getFormData(this);
    var formModal = $('#new-payment-modal');
    data.date = new Date().toISOString();

    $.ajax({
      url: '/api/loans/'+ activeLoan +'/payments/',
      method: 'post',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      success: function() {
        updateLoans();
        formModal.modal('close');
        formModal.find('input[type="text"]').val('');
      },
      error: function(jqXHR, textStatus, errorThrown) {
        sendAlert('Create new payment', jqXHR.responseJSON);
      }
    });
  });

  $(window).ready(function() {
    $('.modal').modal();
    $('.datepicker').datepicker({
      container: 'body',
      format: 'yyyy-mm-dd'
    });

    updateLoans();
  });
})();