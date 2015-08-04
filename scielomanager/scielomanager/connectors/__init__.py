# coding: utf-8
"""Pacote `scielomanager.connectors`.

Um conector é apenas um link entre dois ou mais elementos conectáveis (e.g.,
portas, interfaces etc).
"""
import os

# se apoia na definição da variável __all__ nos módulos.
from .storage import *


_CWD = os.path.dirname(os.path.abspath(__file__))
ES_ARTICLE_MAPPING_PATH = os.path.join(_CWD, 'article_mapping.json')


__all__ = (storage.__all__, ES_ARTICLE_MAPPING_PATH)

