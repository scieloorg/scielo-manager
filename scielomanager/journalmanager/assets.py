from django_assets import Bundle, register

js = Bundle('../static/js/jquery.formset.min.js',
       '../static/js/jquery-formset/jquery.formset.min.js',
       Bundle('../static/js/ajax_enable_disable.js', 
            '../static/js/jquery.popupWindow.js',
            '../static/js/languages.js', 
            '../static/js/multiselect.js',
            '../static/js/tabslideout.js',
            '../static/js/asmselect/jquery.asmselect.js',
            '../static/js/combobox/combobox.js',
            '../static/js/datepicker/datepicker.js',
            '../static/js/datepicker/jquery.ui.datepicker-pt-BR.js',
            '../static/js/jquery/jquery-1.7.1.js',
            '../static/js/jqueryui/jquery-ui.js',
            '../static/js/tabslideout/jquery.tabSlideOut.v1.3.js',
             filters='yui_js'),
             output='bundle.min.js')
register('js', js)