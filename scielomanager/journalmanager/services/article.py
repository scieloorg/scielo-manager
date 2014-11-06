#coding: utf-8
u""" Baseado no padrão `Service layer` descrito em `Patterns of Enterprise
Application Architecture - Martin Fowler.
http://martinfowler.com/eaaCatalog/serviceLayer.html

'[...] estabelece um conjunto de operações disponíveis e coordena a resposta
da aplicação à cada operação.'
"""
import os
import io
import logging
from copy import deepcopy

from lxml import isoschematron, etree

from .. import models


BASIC_ARTICLE_META = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'basic_article_meta.sch')


logger = logging.getLogger(__name__)


# instâncias de isoschematron.Schematron não são thread-safe
base_sch = isoschematron.Schematron(file=BASIC_ARTICLE_META)


def add_from_string(xml_string):
    u""" Cria uma instância de `journalmanager.models.Article`.

    Pode levantar `django.db.IntegrityError` no caso de artigos duplicados,
    TypeError no caso de argumento com tipo diferente de unicode ou
    ValueError no caso de artigos cujos elementos identificadores não estão
    presentes.

    :param xml_string: String de texto unicode.
    :return: aid (article-id) formado por uma string de 32 bytes.
    """
    if not isinstance(xml_string, unicode):
        raise TypeError('Only unicode strings are accepted')

    xml_bstring = xml_string.encode('utf-8')

    try:
        parsed_xml = etree.parse(io.BytesIO(xml_bstring))

    except etree.XMLSyntaxError as exc:
        raise ValueError(u"Syntax error: %s" % (exc.message,))

    except Exception as exc:
        logger.exception(exc)
        raise

    metadata_sch = deepcopy(base_sch)
    if not metadata_sch.validate(parsed_xml):
        logger.debug('Schematron validation error log: %s', metadata_sch.error_log)
        raise ValueError('Missing identification elements')

    new_article = models.Article(xml=xml_bstring)
    new_article.save()

    logger.info('New Article added with aid: %s' % (new_article.aid,))

    return new_article.aid

