$(document).ready(function(){
  $(document).on("click", ".delete-option", function () {
    $(this).parent().remove();
  });

  $('.add-discrete').on('click', function() {
    var field = $(this).parent().parent().find(".discrete-field-label").text();
    $(this).addClass('selected');
    $('#pop-'+field).add($('.overlay')).fadeIn("fast", function(){})
    return false;
  });

  $('.discrete-selection').on('click', function() {
    var field = $(this).parent().parent().children('h5').text();
    var value = $(this).text();
    $("#dvalues-" + field).append(
      '<div class="btn btn-default">' + value + '<span class="close delete-option" style="float:none">&times;</span></div>'
    );
    (function() {
        return this.value + " " + value;
    });
    $('.pop').fadeOut("fast", function() {})
  });

  $('.overlay').on('click', function() {
    $('.pop').fadeOut("fast", function() {})
  });

  $("#search-form").submit(function(eventObj) {
    $(".discrete-field-label").each(function() {
      var field = $(this).text();
      var value = "";
      $('#dvalues-'+field).children('div').each(function () {
        value += this.childNodes[0].nodeValue + ' ';
      });
      $("#dinput-"+field).val(value);
    });
    return true;
  });
});
