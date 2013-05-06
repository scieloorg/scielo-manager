#
#   DEVE SER MANTIDA A ORDEM DOS ARQUIVOS JS e CSS
#

from django_assets import Bundle, register

base_bundle = Bundle('../static/js/jquery/jquery-1.7.1.js',
                     '../static/js/jquery/jquery-ui.js',)

plugins_bundle = Bundle('../static/js/jquery/datepicker.js',
                        '../static/js/jquery/jquery.asmselect.js',
                        '../static/js/jquery/jquery.tabslideout-1.3.js',
                        '../static/js/jquery/jquery.popupwindow.js',
                        '../static/js/jquery/jquery.formset.js')

app_bundle = Bundle('../static/js/bulk_actions.js',
                    '../static/js/languages.js',
                    '../static/js/multiselect.js',
                    '../static/js/toggler.js',
                    '../static/js/tabslideout.js',
                    '../static/js/combobox.js',
                    '../static/js/bootstrap.js')

js = Bundle(base_bundle, plugins_bundle, app_bundle, filters='yui_js', output='bundle.min.js')

register('js', js)

css = Bundle('../static/css/bootstrap.css',
            '../static/css/bootstrap-responsive.css',
            '../static/css/jquery.asmselect.css',
            '../static/css/jquery-ui.css',
            '../static/css/jquery.asmselect.css',
            '../static/css/style.css', filters='yui_css', output='bundle.min.css')

register('css', css)