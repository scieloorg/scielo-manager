/*
 * Get all element with id=datepicker and datepicker - jQquery Plugin
 * Documentation http://jqueryui.com/demos/datepicker/#dropdown-month-year
 *
 */

$(document).ready(function() {

	$('input').filter('.datepicker').datepicker({
					changeMonth: true,
					changeYear: true,
					showButtonPanel: true,
					dateFormat:  "yy-mm-dd"
			});
});