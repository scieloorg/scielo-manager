function get_non_emtpy_formset_rows(){
  var table = $('#other_role_formset');
  var rows = table.find('.dynamic-other_role_formset-form');
  var non_empty_rows = rows.filter(function(){
    return $(this).find('input[type="text"], select').val() != "";
  })
  return non_empty_rows;
}

function clean_formset_rows(){
  var non_empty_rows = get_non_emtpy_formset_rows();
  var delete_links = non_empty_rows.find('a.delete-row');
  /* do delete: */
  delete_links.click();
}

function initialize_formset() {
  $('#other_role_formset tbody tr').formset({
    formCssClass: 'dynamic-other_role_formset-form',
    prefix: 'other_role'
  });
}

function display_or_not_formset() {
  var role = $('#id_role').val();
  if (role == window.other_role_pk) {
    /* show formset */
    $('#other_role_formset_wrapper').slideDown(100);
  } else {
    /* hide formset */
    $('#other_role_formset_wrapper').slideUp(100);
    clean_formset_rows();
  }
}

function bind_role_and_formset () {
  $('#id_role').change(function(){
    display_or_not_formset();
  });
}

$(function() {
  $('.modal').on('shown', function () {
    initialize_formset();
    bind_role_and_formset();
  });
  initialize_formset();
  bind_role_and_formset();
  display_or_not_formset();
});
