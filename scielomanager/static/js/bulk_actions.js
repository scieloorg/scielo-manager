$(document).ready(function() {
  $.each($('table button#action_disable_disable'), function(){
    
    $(this).click(function() {
      $.ajax({
          url: $(this).attr('value'),
          dataType: "json",
          success: function(data){
            if (data.result == 'False'){
              $('#' + data.object_id + ' a:first').addClass("strikethrough");
              $('#' + data.object_id + ' button').removeClass("btn-danger").addClass("btn-success");
              $('#' + data.object_id + ' button').html('enable')
            }else{
              $('#' + data.object_id + ' a:first').removeClass("strikethrough");
              $('#' + data.object_id + ' button').removeClass("btn-success").addClass("btn-danger");
              $('#' + data.object_id + ' button').html('disable')
            }
          }});
      });
  });

  $('#check_all').click(function(){ 
    if ($('#check_all').attr('checked')){
      $('input[name="action"]').attr('checked', true);
    }else{
      $('input[name="action"]').attr('checked', false);
    }
  });

  $('a#bulk_action_enable').click(function(){ 
    $("#bulk_action").attr('action', $("a#bulk_action_enable").attr('rel'));
    $("#bulk_action").submit();
  });

  $('a#bulk_action_disable').click(function(){ 
    $("#bulk_action").attr('action', $("a#bulk_action_disable").attr('rel'));
    $("#bulk_action").submit();
  });

});