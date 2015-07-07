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

/*** Campo ORCID: validação pela API de Orcid ***/

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

$('#id_orcid').on('input', function(event) {
  /* Para cada mudança no campo '#id_orcid':
   * - verifica se o tamanho esta certo (20 chars contando os 4 "-")
   * - verifica se atende a regex (o ultimo digito pode ser um "X", ver referencia)
   * - verifica se o checksum é valido com a função: is_valid_orcid_checksum(...)
   *
   * Se atendes todos os requisitos, ainda é feito um request ajax contra a API de ORCID.
   *
   * As vezes pelo throttling, este paso de validação não esta disponível.
   * Tem casos que a API retorna 404 para alguns ordid válidos. misterio! (exemplo: 0000-0002-6444-9718)
   *
   * Se o conteúdo do campo é vazio, então é considerado como válido também.
   *
   * referencias:
   * - http://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier
   * - https://orcid.github.io/XSD/XSD_1.2_Documentation/orcid-message-1.2.html
   */

  var orcid_field = $(this);
  var orcid_input = this.value.trim();
  var orcid_lenght = orcid_input.length;

  if (orcid_lenght > 0) {
    var re = /\d{4}-\d{4}-\d{4}-\d{3}[\d|X]/;
    if (orcid_lenght < 20 && re.test(orcid_input) && is_valid_orcid_checksum(orcid_input)) {
      var orcid_api_url = "http://pub.orcid.org/v1.2/" + orcid_input + "/orcid-bio";
      orcid_field.attr("disabled", "disabled");

      $.ajax({
          url: orcid_api_url,
          contentType: 'application/vnd.orcid+xml',
          dataType: 'xml',
        })
        .done(function( xml_data ) {
          var profile_type = $(xml_data).find('orcid-profile').attr('type');
          if (profile_type === 'user') {
            display_validation_result(orcid_field, true);
          } else {
            /* o tag <orcid-profile> no vem na resposta ou não é do tipo user! */
            display_validation_result(orcid_field, false);
          }
        })
        .fail(function( jqxhr, textStatus, error ) {
          display_validation_result(orcid_field, false);
        })
        .always(function(){
          orcid_field.removeAttr('disabled');
      });

    } else {
      /* input de tamanho errado, ou formato errado, ou checksum inválido */
      display_validation_result(orcid_field, false);
    }
  } else {
    /* input pode ser vazio */
    display_validation_result(orcid_field, true);
  }
});
