$(document).ready(function(){

  var offset = 0;
  var searching = false;

  function pullResults (amount, offset) {
    $("#results-done").css("display", "none");
    $(".loader").css("display", "block");
    $("#amount-input").val(amount);
    $("#offset-input").val(offset);

    $.get( "/api/query/" + project_name + "?" + $('#search-form').serialize(), function( data_str ) {
        $(".loader").css("display", "none");
        console.log(data_str);
        var data = JSON.parse( data_str );
        var image_div = $("#result-images-div");
        $("#total-results").html(data["total"] + " results")

        if (Object.keys(data["results"]).length == 0) {
          $("#results-done").css("display", "block");
          searching = false;
          return;
        }

        for (var i in data["results"]) {
          var item = data["results"][i];
          var image = $("<img></img>")
                        .attr("src", item["img"])
                        .attr("height", "150px")
                        .attr("width", "150px")
                        .addClass("result-image");
          var imageInfo = $("<div></div>")
                            .addClass("image-info")
                            .append("<div>Id</div>");
          for (var j in item["id"]) {
            imageInfo.append("<div>" + j + " : " + item["id"][j] + "</div>");
          }
          imageInfo.append("<div>Fields</div>");
          for (var j in item["numeric"]) {
            imageInfo.append("<div>" + j + " : " + item["numeric"][j] + "</div>");
          }
          for (var j in item["discrete"]) {
            imageInfo.append("<div>" + j + " : " + item["discrete"][j] + "</div>");
          }
          var imageLabel = $("<span></span>")
                            .append(image)
                            .append(imageInfo);
          image_div.append(imageLabel);
        }
    });
  }

  $(document).on("click", ".delete-option", function () {
    $(this).parent().remove();
  });

  $(document).on('click', '.result-image', function() {
    $('#detailed-info').empty();
    $('#detailed-image').attr("src", $(this).attr("src"));
    var info = $(this).parent().find('.image-info').clone();
    info.appendTo($('#detailed-info'));
    info.css("display", "block");
    $('.detail-pop').add($('.overlay')).fadeIn("fast");
  });

  $('.add-discrete').on('click', function() {
    var field = $(this).parent().parent().find(".discrete-field-label").text();
    $(this).addClass('selected');
    $('#pop-'+field).add($('.overlay')).fadeIn("fast");
  });

  $('.discrete-selection').on('click', function() {
    var field = $(this).parent().parent().children('h5').text();
    var value = $(this).text();
    $("#dvalues-" + field).append(
      '<div class="btn btn-default">' + value + '<span class="close delete-option" style="float:none">&times;</span></div>'
    );
    $('.pop').fadeOut("fast");
  });

  $('.overlay').on('click', function() {
    $('.pop').fadeOut("fast");
  });

  $("#search-button").on('click', function() {
    console.log($('#search-form').serialize());
    $(".discrete-field-label").each(function() {
      var field = $(this).text();
      var value = "";
      $('#dvalues-'+field).children('div').each(function () {
        value += this.childNodes[0].nodeValue + ' ';
      });
      $("#dinput-"+field).val(value);
    });
    $(".has-error").removeClass("has-error");
    if (!$('#search-form')[0].checkValidity()) {
      $(".numeric-input").each(function() {
        if (!$(this)[0].checkValidity()) {
          $(this).parent().closest(".form-group").addClass("has-error");
        }
      });
    } else {
      searching = true;
      $("#result-images-div").empty();
      pullResults(100, 0);
      offset = 100;
    }
  });

  $(window).scroll(function() {
    if(searching && $(window).scrollTop() == $(document).height() - $(window).height()) {
      pullResults(50, offset);
      offset += 50;
    }
  });

});
