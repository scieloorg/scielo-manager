MULTILINGUAL_FIELDS = {};

$(document).ready(function(){
    // Prepares multilingual inputs
    $('.multilingual').each(function(){
        // Gets field name
        var f_name = $(this).find('.en').find('input, textarea').attr('name');

        // Creates floating combo to select second language
        var sel = $('<div class="sel"><b>Second language:</b> </div>').prependTo($(this));

        for (var i=0; i<MULTILINGUAL_FIELDS['available_languages'].length; i++) {
            if (MULTILINGUAL_FIELDS['available_languages'][i] !== 'en') {
                $('<a href="javascript: void(0)">'+MULTILINGUAL_FIELDS['available_languages'][i]+'</a>')
                    .appendTo(sel).click(function(){
                    var new_lang = $(this).text();
                    $(this).parents('.multilingual').find('.multilingual-value').each(function(){
                        if ($(this).hasClass('en') || $(this).hasClass(new_lang)) {
                            $(this).show();
                        } else {
                            $(this).hide();
                        }
                    });
                });
                sel.append('; ');
            }
        }
    });
});

