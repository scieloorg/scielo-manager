#coding: utf-8
import os
import weakref
import datetime
import re
import unicodedata
import logging

from thrift import clients

logger = logging.getLogger(__name__)

REGEX_ISSN = re.compile(r"^[0-9]{4}-[0-9]{3}[0-9xX]$")


def articlemeta_server():
    try:
        server = 'articlemeta.scielo.org:11720'
        host = server[0]
        port = int(server[1])
    except:
        logger.warning('Error defining Article Meta thrift server, assuming default server articlemeta.scielo.org:11720')
        host = 'articlemeta.scielo.org'
        port = 11720

    return clients.ArticleMeta(host, port)


def ckeck_given_issns(issns):
    valid_issns = []

    for issn in issns:
        if not REGEX_ISSN.match(issn):
            continue
        valid_issns.append(issn)

    return valid_issns
