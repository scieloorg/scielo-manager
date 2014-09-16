$(function() {

  /* hack to reload ajax content, and avoid caching trap */
  $('.modal').on('hidden', function() { $(this).removeData(); })
  $('.modal').on('shown', function () {
    $('input').addClass('span12');
    $(".chzn-select").chosen({
      no_results_text: "{% trans 'No results found for' %}:",
      width: "100%",
    });
  })

  /* actions: */
  $('.btn-resize-full').click(function(event) {
    event.preventDefault();
    var $self = $(this);
    var modal = $self.parents('.modal');
    modal.addClass('large')
         .addClass('wide')
         .find('.btn-resize-small').show();
    $self.hide();
  });

  $('.btn-resize-small').click(function(event) {
    event.preventDefault();
    var $self = $(this);
    var modal = $self.parents('.modal');
    modal.removeClass('large')
         .removeClass('wide')
         .find('.btn-resize-full').show();
    $self.hide();
  });

  $('.btn-submit').click(function(event) {
    event.preventDefault();
    var modal = $(this).parents('.modal');
    /* find a form tag inside modal-body, and trigger submit event, then hide modal */
    modal.find('.modal-body').find('form').submit();
  });

});
