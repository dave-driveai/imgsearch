$(document).ready(function(){

  $('.delete-button').on('click', function() {
    var project = $(this).parent().find('.project-name').text();
    $.post( "/api/delete/" + project, function() {
      location.reload();
    });
  });

});
