#
#   DEVE SER MANTIDA A ORDEM DOS ARQUIVOS JS e CSS
#

from django_assets import Bundle, register

base_bundle = Bundle('../static/js/jquery/jquery-1.8.3.js',
                     '../static/js/jquery/jquery-ui.js')

minify_bundle = Bundle('../static/js/angular/angular.min.js',
                       '../static/js/bootstrap-filestyle.min.js')

plugins_bundle = Bundle('../static/js/jquery/jquery.asmselect.js',
                        '../static/js/jquery/jquery.popupwindow.js',
                        '../static/js/jquery/jquery.formset.js',
                        '../static/js/angular/ui-bootstrap-tpls-0.4.0.js',
                        '../static/js/jquery/select2.js')

app_bundle = Bundle('../static/js/bulk_actions.js',
                    '../static/js/languages.js',
                    '../static/js/multiselect.js',
                    '../static/js/combobox.js',
                    '../static/js/bootstrap.js')


js = Bundle(base_bundle, minify_bundle, plugins_bundle, app_bundle, filters='yui_js', output='js/bundle.min.js')

register('js', js)

css = Bundle('../static/css/bootstrap.css',
            '../static/css/bootstrap-responsive.css',
            '../static/css/jquery.asmselect.css',
            '../static/css/jquery-ui.css',
            '../static/css/jquery.asmselect.css',
            '../static/css/select2.css',
            '../static/css/style.css', filters='yui_css', output='css/bundle.min.css')

register('css', css)
