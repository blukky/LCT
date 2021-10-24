/* startrek Single Theme Initializer Script 

Table of Contents

01. Single Theme Initializer
*/

/* 01. Single Theme Initializer */

(function ($) {
  if ($().dropzone) {
    Dropzone.autoDiscover = false;
  }

  var direction = "ltr";
  var radius = "rounded";

  if (typeof Storage !== "undefined") {
    if (localStorage.getItem("startrek-direction")) {
      direction = localStorage.getItem("startrek-direction");
    } else {
      localStorage.setItem("startrek-direction", direction);
    }
    if (localStorage.getItem("startrek-radius")) {
      radius = localStorage.getItem("startrek-radius");
    } else {
      localStorage.setItem("startrek-radius", radius);
    }
  }

  $("body").addClass(direction);
  $("html").attr("dir", direction);
  $("body").addClass(radius);
  $("body").startrek();
})(jQuery);
