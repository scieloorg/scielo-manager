# coding: utf-8
"""Pacote `scielomanager.connectors`.

Um conector é apenas um link entre dois ou mais elementos conectáveis (e.g.,
portas, interfaces etc).
"""
# se apoia na definição da variável __all__ nos módulos.
from .storage import *


__all__ = (storage.__all__, )

