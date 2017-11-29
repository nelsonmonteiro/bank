$(document).ready(function(){
  $('.scroll-to-div').click(function(e) {
    e.preventDefault();
    var divId = $(this).attr('scroll-id') || $(this).attr('href');
    var offset = $(this).attr('scroll-offset') || 0;
    var duration = $(this).attr('scroll-duration') || 500;

    if (divId) {
      divId = divId.charAt(0) !== '#' && divId.charAt(0) !== '.' ? '#'+divId : divId;
      scrollToDiv(divId, offset, duration);
    }
  });
});

function getFormData(formId) {
  return $(formId).serializeArray().reduce(function(obj, item) {
    obj[item.name] = item.value;
    return obj;
  }, {});
}

function scrollToDiv(divId, offset, duration) {
  $('html, body').animate({
    scrollTop: $(divId).offset().top - (offset || 0)
  }, duration || 500);
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});