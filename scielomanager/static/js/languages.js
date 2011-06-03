$(document).ready(function(){
    $("#lang_en").click(function() {
        $("#form_language input#language").val('en');
        $("#form_language").submit();
    });
    $("#lang_pt-BR").click(function() {
        $("#form_language input#language").val('pt-br');
        $("#form_language").submit();
    });
    $("#lang_es").click(function() {
        $("#form_language input#language").val('es');
        $("#form_language").submit();
    });
});
