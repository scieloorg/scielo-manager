$(document).ready(function(){
    $("#lang_options").change(function () {
        var selected = $(this).val();
        $("#form_language input#language").val(selected);
        $("#form_language").submit();
    });
});
