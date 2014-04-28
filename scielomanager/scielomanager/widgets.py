# coding: utf-8
from django.contrib.admin.widgets import AdminFileWidget


class AdminImageWidget(AdminFileWidget):
    template_with_initial = u'%(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    template_with_clear = u'<br/><br/><label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s %(clear)s</label>'
