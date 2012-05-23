/*
 * Get all select with multiple atribute and apply asmSelect - jQquery Plugin
 * Documentation http://www.ryancramer.com/projects/asmselect/
 *
 */

$(document).ready(function() {
    $("select[multiple]").asmSelect({
        sortable: true,
        animate: true,
        addItemTarget: 'top',
        hideWhenAdded: true,
    });
});

function updateSelect(win, newid, name, component){

  var $option = $("<option></option>").text(name).attr("selected", true);
  $option.val(newid);
  $('#' + component).append($option).change();
  win.close();

}