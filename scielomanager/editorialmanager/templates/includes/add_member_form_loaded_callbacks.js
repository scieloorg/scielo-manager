{% load i18n %}

/* Este codigo contém callbacks que pode ser executado em duas situações:
 * - Quando o formulario de adicionar um Board Member é carregado no modal (após ser disparado o evento: 'loaded')
 * - QUando o formulario de adicionar um Board Member é carregado numa página simples, (não no modal, nem com ajax.load)
 */

/*** campo Institution: AUTOCOMPLETE: ***/

$('#id_institution').devbridgeAutocomplete({
  serviceUrl: "{{SETTINGS.WAYTA_URL}}{{SETTINGS.WAYTA_PATH}}institution",
  dataType: 'jsonp',
  paramName: 'q',
  noCache: true,
  params: {'accuracy': 3},
  minChars: 3,
  transformResult: function(response) {
    return {
      query:'q',
      suggestions: $.map(response.choices, function(dataItem) {
          return {
            value: dataItem.value,
            data: {
              'country': dataItem.country,
              'city': dataItem.city,
              'state': dataItem.state,
              'iso3166': dataItem.iso3166
            }
          };
      })
    }
  },

  formatResult: function (suggestion, currentValue) {
    return '<b>{% trans 'Institution' %}:</b> ' + suggestion.value + '</br>' +
           '<b>{% trans 'City' %}:</b> ' + suggestion.data.city + '</br>' +
           '<b>{% trans 'State' %}:</b> ' + suggestion.data.state + '</br>' +
           '<b>{% trans 'Country' %}:</b> ' + suggestion.data.country;
  },

  onSelect: function (suggestion) {
    $('#id_city').val(suggestion.data.city)
    $('#id_state').val(suggestion.data.state)

    $('#id_country option').each(function() {
      if (this.value == suggestion.data.iso3166){
          this.selected = this.text;
          $(".chzn-select").trigger("chosen:updated");
      }
    });
  },

  appendTo: $('#selection')

});//devbridgeAutocomplete

/*** Campo ORCID: validação Orcid ***/

function is_valid_orcid_checksum(input_string){
  /* Calcula o checksum a partir do orcid que vem no parametro: "input_string".
   * Se o checksum é igual ao ultimo digito do orcid, retorna: true.
   *
   * referencia:
   *   http://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier
   */
  var total = 0, digit = 0;
  var cleaned = input_string.trim().replace(/-/g, '');
  var last_digit = cleaned.charAt(cleaned.length-1);
  cleaned = cleaned.substring(0, cleaned.length -1);

  for (var i = 0; i < cleaned.length; i++) {
    digit = parseInt(cleaned.charAt(i), 10);
    total = (total + digit) * 2;
  }

  var remainder = total % 11;
  var calculated_checksum = (12 - remainder) % 11;

  if (calculated_checksum == 10){
    calculated_checksum = "X";
  }

  return calculated_checksum == last_digit;
}

function display_validation_result(field, is_valid){
  /* - adiciona no DOM as classes de "error" ou "success"
   *   para mostrar para o usuário o resultado da validação
   * - adiciona o background com o icone verde (ok) ou vermelho (error)
   */
  if (is_valid) {

    field.parents('.control-group')
      .removeClass('error')
      .addClass('success');
    field.removeClass('invalid-input-icon')
      .addClass('valid-input-icon');

  } else {

    field.parents('.control-group')
      .removeClass('success')
      .addClass('error');
    field.removeClass('valid-input-icon')
      .addClass('invalid-input-icon');

  }
}


function display_orcid_link(field, orcid_id){
  /* Adiciona um link para que o usurário acesse o perfil no site orchid.org
   */
  var target_url = 'http://orcid.org/' + orcid_id; /* sem barra no final, porque se não manda pro login */
  var link = $('<a />').attr({
    'href': target_url,
    'title': target_url,
    "target": "_blank",
  }).html(target_url);
  var field_container = field.parents('.control-group'); /* control-group */
  var link_placeholder = field_container.find('#orcid_link_placeholder');

  if (link_placeholder.size() > 0 ) {
    link_placeholder.html(link);
  } else {
    /* link placeholder not found, create a new one */
    link_placeholder = $('<span />').attr({
      'id': 'orcid_link_placeholder',
      'class': 'pull-right',
    }).html(link);
    field_container.append(link_placeholder);
  }
}

function clear_orcid_link(field){
  var link_placeholder = field.parents('.control-group').find('#orcid_link_placeholder');
  link_placeholder.html('');
}

function has_valid_orcid(orcid_id){
  /* Validação do formato do string: "orcid_id" segundo os criterios:
   * - verifica se o tamanho esta certo (19 chars contando os 3 "-")
   * - verifica se atende a regex (o ultimo digito pode ser um "X", ver referencia)
   * - verifica se o checksum é valido com a função: is_valid_orcid_checksum(...)
   *
   * Se atende as 3 condições retorna true.
   *
   * referencias:
   * - http://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier
   */
  var re = /^\d{4}-\d{4}-\d{4}-\d{3}[\d|X]$/;
  return re.test(orcid_id) && is_valid_orcid_checksum(orcid_id);
}

$('#id_orcid').on('input', function(event) {
  /* Para cada mudança no campo '#id_orcid':
   * Valida o fomarto do valor inserido no campo (has_valid_orcid(...)).
   * - Se for válido, é criado um link para que o usuário possa validar visualmente.
   * - Se o conteúdo do campo é vazio, então é considerado como válido também.
   */

  var orcid_field = $(this);
  var orcid_input = this.value.trim();

  clear_orcid_link(orcid_field);

  if (orcid_input.length > 0) {
    if (has_valid_orcid(orcid_input)) {
      /* input tem formato ok, mostrar link para o usuário  */
      display_validation_result(orcid_field, true);
      display_orcid_link(orcid_field, orcid_input);
    } else {
      /* input de tamanho errado, ou formato errado, ou checksum inválido */
      display_validation_result(orcid_field, false);
    }
  } else {
    /* input pode ser vazio, isso é válido, mas não vai ter link! */
    display_validation_result(orcid_field, true);
  }
});
