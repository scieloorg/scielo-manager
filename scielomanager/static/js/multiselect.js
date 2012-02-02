/*
 * Get all select with multiple atribute and apply asmSelect - jQquery Plugin
 * Documentation http://www.ryancramer.com/projects/asmselect/
 *
 */

$(document).ready(function() {
    $("select[multiple]").asmSelect({
        sortable: false,
        animate: true,
        addItemTarget: 'top'
    });
});