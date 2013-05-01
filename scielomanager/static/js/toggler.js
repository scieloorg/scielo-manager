/*
 * Get all div with class=toggler and apply show/hide
 */

$(document).ready(function() {

  $('.toggler').each(function(){

    var $show_hide_link = $('<a class="icon-chevron-down"></a>')
          .attr("href", "javascript:void(0)")
          .click(function() {
            $(this).next().toggle('slow', function(){
              $(this).prev().toggleClass('icon-chevron-down icon-chevron-up')
            });
          });

    $(this).before($show_hide_link);

  });

});