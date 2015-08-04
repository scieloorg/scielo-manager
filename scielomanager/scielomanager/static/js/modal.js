// include onetime, somewhere
// this patch trigger a new event "loaded" when jquery.load function receive the ajax response
// more context about the fix: https://github.com/twbs/bootstrap/pull/6846

(function(){
    $.fn.jqueryLoad = $.fn.load;

    $.fn.load = function(url, params, callback) {
        var $this = $(this);
        var cb = $.isFunction(params) ? params: callback || $.noop;
        var wrapped = function(responseText, textStatus, XMLHttpRequest) {
            cb(responseText, textStatus, XMLHttpRequest);
            $this.trigger('loaded');
        };

        if ($.isFunction(params)) {
            params = wrapped;
        } else {
            callback = wrapped;
        }

        $this.jqueryLoad(url, params, callback);

        return this;
    };
})();


$(function() {

  /* hack to reload ajax content, and avoid caching trap */
  $('.modal').on('hidden', function() {
    $(this).removeData();
    $('.btn-resize-small').click();
  });
  $('.modal').on('loaded', function () {
    $(this).find('input').addClass('span12');
    var chosenOptions = defaultChosenOptions;
    chosenOptions['width'] = "100%";
    $(this).find(".chzn-select").chosen(chosenOptions);
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
