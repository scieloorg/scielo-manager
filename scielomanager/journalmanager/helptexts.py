# coding: utf-8
from django.utils.translation import ugettext_lazy as _

from scielomanager import settings

GLOSSARY_URL = settings.DOCUMENTATION_BASE_URL +'/glossary.html#'


JOURNALPARALLELTITLES__FORM = _("""Enter parallel titles in accordance with the sequence and
    typography in which they appear on the title page or its substitute.
    <a href="%sterm-parallell-titles" target="_blank">Read more</a>""" % GLOSSARY_URL)