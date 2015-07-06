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
                        '../static/js/jquery/select2.js',
                        '../static/js/jquery/jquery.autocomplete.js')

app_bundle = Bundle('../static/js/bulk_actions.js',
                    '../static/js/languages.js',
                    '../static/js/multiselect.js',
                    '../static/js/combobox.js',
                    '../static/js/bootstrap.js',
                    '../static/js/chosen.jquery.js',
                    '../static/js/modal.js',
                    )


js = Bundle(base_bundle, minify_bundle, plugins_bundle, app_bundle, filters='yui_js', output='js/bundle.min.js')

register('js', js)

css = Bundle('../static/css/bootstrap.css',
             '../static/css/bootstrap-responsive.css',
             '../static/css/jquery.asmselect.css',
             '../static/css/jquery-ui.css',
             '../static/css/jquery.asmselect.css',
             '../static/css/select2.css',
             '../static/css/chosen.css',
             '../static/css/style.css', filters='yui_css', output='css/bundle.min.css')

register('css', css)

# codemirror
codemirror_css = Bundle(
            '../static/css/codemirror/lib/codemirror.css',
            '../static/css/codemirror/addon/fold/foldgutter.css',
            '../static/css/codemirror/addon/display/fullscreen.css',
            '../static/css/codemirror/addon/dialog/dialog.css',
            '../static/css/codemirror/custom_styles.css',
            filters='yui_css',
            output='css/codemirror_bundle.min.css')

register('codemirror_css', codemirror_css)

codemirror_js = Bundle(
            '../static/js/jquery/jquery-1.8.3.js',
            '../static/js/codemirror/lib/codemirror.js',
            '../static/js/codemirror/mode/xml/xml.js',
            '../static/js/codemirror/addon/fold/foldcode.js',
            '../static/js/codemirror/addon/fold/foldgutter.js',
            '../static/js/codemirror/addon/fold/brace-fold.js',
            '../static/js/codemirror/addon/fold/xml-fold.js',
            '../static/js/codemirror/addon/fold/comment-fold.js',
            '../static/js/codemirror/addon/display/fullscreen.js',
            '../static/js/codemirror/addon/selection/active-line.js',
            '../static/js/codemirror/addon/edit/matchtags.js',
            '../static/js/codemirror/addon/dialog/dialog.js',
            '../static/js/codemirror/addon/search/searchcursor.js',
            '../static/js/codemirror/addon/search/search.js',
            '../static/js/codemirror/addon/search/goto-line.js',
            filters='yui_js',
            output='js/codemirror_bundle.min.js')

register('codemirror_js', codemirror_js)
