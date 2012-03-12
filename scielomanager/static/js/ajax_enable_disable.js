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
        }});//ajax
    });//click
});//each

});//load
