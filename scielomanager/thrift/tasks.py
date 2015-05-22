# coding: utf-8
from scielomanager.celery import app
from django.db import IntegrityError, transaction

from journalmanager import services


@app.task(throws=(IntegrityError, ValueError))
def add_article(xml_string, raw):
    """
    Levanta as exceções: 1) IntegrityError quando o XML já foi registrado
    anteriormente e 2) ValueError quando o XML não contém metadados suficientes
    para a sua identificação.
    """
    with transaction.commit_on_success():
        return services.article.add_from_string(xml_string, raw)

