// Modal

$(document).ready(function() {

  $("a[data-target=modal]").click(function(event) {
      event.preventDefault();
      var target = $(this).attr("href");
      $("#modal .modal-body").load(target, function() {
           $("#modal").modal("show");
      });
  });

});
