function toPage(page) {
    var paramsStr = window.location.search.substring(1),
        params = paramsStr.split('&'),
        ret = "",
        i;

    var newParams = params.filter(function(item, idx) {
        return item.split('=')[0] !== "page";
    });
    newParams.push("page=" + page)

    for (i = 0; i < newParams.length; i++) {
        ret += newParams[i];
        if (i != newParams.length-1) {
          ret += '&';
        }
    }
    document.location.href = window.location.href.split('?')[0] + '?' + ret;
};


$(document).ready(function(){
  $(document).on("click", ".delete-option", function () {
    $(this).parent().remove();
  });

  $('.result-image').on('click', function() {
    $('#detailed-image').attr("src", $(this).attr("src"));
    var info = $(this).parent().find('.image-info').clone();
    info.appendTo($('#detailed-info'));
    info.css("display", "block");
    $('.overlay').fadeIn("fast", function(){});
  });

  $('.overlay').on('click', function() {
    $('.overlay').fadeOut("fast", function(){
      $(this).find('#detailed-info').empty();
    });
  });

  $('#prev-page').on('click', function() {
    toPage(parseInt($('#current-page-no').text()) - 1);
  });

  $('#next-page').on('click', function() {
    toPage(parseInt($('#current-page-no').text()) + 1);
  });

  $('#go-page-button').on('click', function() {
    toPage($('#page-input').val());
  });
});
