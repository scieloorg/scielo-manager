/*
 * Get all select with multiple atribute and apply asmSelect - jQquery Plugin
 * Documentation http://www.ryancramer.com/projects/asmselect/
 *
 */

$(document).ready(function() {

    if(!$("select[multiple]").attr('chosen')){
      $("select[multiple]").asmSelect({
          sortable: true,
          animate: true,
          addItemTarget: 'bottom',
          hideWhenAdded: true
      });
    }else{
      $("select[chosen]").select2({placeholder: "Select an item", width: '1100px'});
    }

});

function updateSelect(win, newid, name, component){

  var $option = $("<option></option>").text(name).attr("selected", true);
  $option.val(newid);
  $('#' + component).append($option).change();
  win.close();

}