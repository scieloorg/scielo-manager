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

from lxml import isoschematron, etree

from .. import models


BASIC_ARTICLE_META = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'basic_article_meta.sch')


metadata_sch = isoschematron.Schematron(file=BASIC_ARTICLE_META)
logger = logging.getLogger(__name__)


def add_from_string(xml_string, raw=True):
    u""" Cria uma instância de `journalmanager.models.Article`.

    Pode levantar `django.db.IntegrityError` no caso de artigos duplicados,
    TypeError no caso de argumento com tipo diferente de unicode ou
    ValueError no caso de artigos cujos elementos identificadores não estão
    presentes.

    :param xml_string: String de texto unicode.
    :param raw: Bool que indica que `xml_string` ingressou no sistema como XML SciELO PS.
    :return: aid (article-id) comprised of 32-byte string.
    """
    if not isinstance(xml_string, unicode):
        raise TypeError('Only unicode strings are accepted')

    xml_bstring = xml_string.encode('utf-8')

    try:
        parsed_xml = etree.parse(io.BytesIO(xml_bstring))

    except etree.XMLSyntaxError as exc:
        raise ValueError(u"Syntax error: %s" % (exc.message,))

    except Exception as exc:
        logger.info(exc)
        raise

    if not metadata_sch.validate(parsed_xml):
        raise ValueError('Missing identification elements')

    # O valor de Article.is_generated ficou invertido em relação à interface
    # pública. Acontece nas melhores famílias.
    new_article = models.Article(xml=xml_bstring, is_generated=not raw)
    new_article.save()

    logger.info('New Article added: %s' % (new_article,))

    return new_article.aid

