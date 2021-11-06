jQuery(function($) {
  $('#wozd > li > h3').click(function() {

    if ($(this).parent().find('p').length) {
      $(this).parent().find('p').slideToggle(200);

      return false;
    }

  });
});