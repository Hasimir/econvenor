/*!
 * 
 * eConvenor base JavaScript
 * 
 */


/* Get CSRF token
-------------------------------------------------- */

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

var csrftoken = getCookie('csrftoken');


/* Enable jQuery UI functions
-------------------------------------------------- */

$(function enableJQueryUIFeatures() {
  $('.datepicker').datepicker({
    dateFormat: 'dd M yy',
    onClose: function() {
      $(this).valid();
    },  
  });
  $( '.sortable' ).sortable({
    axis: 'y',
    containment: 'parent',
    tolerance: 'pointer',
  });
  $( '.spinner' ).spinner({ min: 0, max: 600, });
});


/* Enable Bootstrap functions
-------------------------------------------------- */
$(function enableBootstrapFeatures() {
  $('.tltip').tooltip({
    placement: 'bottom',
    delay: { show: 500, hide: 100 }
  });
});


/* Enable Timepicker
-------------------------------------------------- */
$(function enableTimepicker() {
  $('.timepicker').timepicker({
    'timeFormat': 'g:i a',
    'step': 15,
    'scrollDefaultTime': '9:15 am',
  });
});


/* Enable automatic vertical scrolling to a target
-------------------------------------------------- */

$("html").on("click", ".sidebar-heading", function(event){ 
  var $anchor = $(this);
  $("html").stop().animate({
    scrollTop: $($anchor.attr('href')).offset().top-90
  }, 1000);
  event.preventDefault();
});


/* Enable zooming of images
-------------------------------------------------- */

$(document).on("click", ".zoom-button", function(){ 
  var current_zoom = $('.zoomable').attr('width');
  current_zoom = current_zoom.slice(0, -1);
  current_zoom = parseInt(current_zoom, 10)
  var zoom_direction = $(this).attr('id');
  if (zoom_direction == 'zoom_out') {
    new_zoom = current_zoom - 10;
    } else {
    new_zoom = current_zoom + 10;
    }
  var zoom = new_zoom + '%'
  $('.zoomable').attr('width', zoom);
});


/* Clear distribution list checkboxes when required
-------------------------------------------------- */

$(document).on("click", ".checkbox #all_participants", function(){ 
  var checkbox_status = $(this).prop('checked');
  if (checkbox_status == true) {
    $(".individual-checkbox").prop('checked', false);
  };
});

$(document).on("click", ".individual-checkbox", function(){ 
  var checkbox_status = $(this).prop('checked');
  if (checkbox_status == true) {
    $(".checkbox #all_participants").prop('checked', false);
  };
});


/* Populate deletion confirmation modal
-------------------------------------------------- */

$(document).on("click", ".delete-button", function(event){ 
  event.preventDefault();
  var instruction = $(this).attr('id');
  var description = $(this).attr('name');
  var confirmation_message = '<p>You are about to delete this record:\
    <br/><br/><strong>' + description + '</strong><br/><br/>\
    This action cannot be undone.<br/><br/>Continue?</p>';
  $('.modal-button').attr('value', instruction);
  $(".modal-body").html( confirmation_message );
  $('#delete_modal').modal();
});


/* Enable dynamic sidebar navigation
-------------------------------------------------- */

$(function() {
  $("#leftsidebar").metisMenu();
});

$(function removeActiveItemCarat() {
  $(".active a:nth-child(1) i:nth-child(2)").toggleClass("fa-angle-down fa-angle-up");
});

$(".sidebar-item ").click(function() {
  	var item_clicked_arrow = $(this).children().first().children().next()
  	$("i").filter(".fa-angle-up").not(item_clicked_arrow).toggleClass(
  	  "fa-angle-down fa-angle-up"
  	);
  	item_clicked_arrow.toggleClass("fa-angle-down fa-angle-up");
});


/* Character counting and limiting plugin 
-------------------------------------------------- */

$(function() {

  $.fn.charactercounter = function(){

    var char_counter_div = $("<div class='characterCounterDisplay pull-right'/>");
    this.before(char_counter_div);
    $(".characterCounterDisplay").hide();

    this.on("focus keyup", function(){ 
      /* A newline character counts as two characters, so the number of newline
         characters must be added to the 'normal' character count */
      var newlines = $(this).val().match(/\n/g);
      if (newlines) {
          var newline_count = newlines.length;
      } else {
          var newline_count = 0;
      };
      var char_count = $(this).val().length + newline_count;
      var maximum_length = $(this).attr('maxlength');
      var warning_length = parseInt(maximum_length * 0.18) * 5
      var chars_remaining = maximum_length - char_count;
      if (char_count == 0) {
        var message = "<p>" + chars_remaining + ' characters maximum</p>'
      } else {
        var message = "<p>" + chars_remaining + ' characters remaining</p>'
      };
      $(".characterCounterDisplay").html( message );
      if ((char_count >= warning_length) || (char_count === 0)) {
        ($(this)).prev().addClass("red");
      } else {
        ($(this)).prev().removeClass("red");  
      };
      if (char_count > maximum_length) {
        $(this).value = $(this).value.substr(0, maxlength);
        chars = limit;
      };
      $($(this)).prev().show();
    });

    this.on("blur", function(){ 
      $(".characterCounterDisplay").hide();
    });

  };
});

/* Enable character counter and limiter
-------------------------------------------------- */

$(function() {
  $('.charactercounter').charactercounter();
});
