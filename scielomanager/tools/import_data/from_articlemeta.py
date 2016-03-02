# coding: utf-8
import os
import argparse
import logging

from xylose.scielodocument import Journal, Issue

import utils
from importer import Catalog

logger = logging.getLogger(__name__)


def _config_logging(logging_level='INFO', logging_file=None):

    allowed_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.setLevel(allowed_levels.get(logging_level, 'INFO'))

    if logging_file:
        hl = logging.FileHandler(logging_file, mode='a')
    else:
        hl = logging.StreamHandler()

    hl.setFormatter(formatter)
    hl.setLevel(allowed_levels.get(logging_level, 'INFO'))

    logger.addHandler(hl)

    return logger


class Importer(object):

    def __init__(self, collection_from, collection_to, user=None, issns=None):

        self._articlemeta = utils.articlemeta_server()
        self.collection_from = collection_from
        self.issns = issns
        self.catalog = Catalog(collection_to, user=user)

    def run(self):
        for item in self.items():
            self.catalog.load_issue(item)

    def items(self):

        if not self.issns:
            self.issns = [None]

        for issn in self.issns:
            for data in self._articlemeta.issues(
                    collection=self.collection_from, issn=issn):
                logger.debug(u'Lendo fascículos (%s-%s) do periódico %s - %s' % (
                    data.type, data.label, data.journal.title, data.journal.scielo_issn))

                yield data


def main():
    parser = argparse.ArgumentParser(
        description='Importa metadados de catalogos SciELO do modelo legado para o SciELO Manager'
    )

    parser.add_argument(
        'issns',
        nargs='*',
        help='ISSN\'s separated by spaces'
    )

    parser.add_argument(
        '--collection_from',
        '-c',
        help='Collection Acronym'
    )

    parser.add_argument(
        '--collection_to',
        '-t',
        help='Collection Acronym'
    )

    parser.add_argument(
        '--logging_file',
        '-o',
        help='Full path to the log file'
    )

    parser.add_argument(
        '--logging_level',
        '-l',
        default='DEBUG',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logggin level'
    )

    args = parser.parse_args()
    _config_logging(args.logging_level, args.logging_file)
    logger.info(u'Importando dados da coleção: %s' % args.collection_from)

    issns = None
    if len(args.issns) > 0:
        issns = utils.ckeck_given_issns(args.issns)

    try:
        importer = Importer(args.collection_from, args.collection_to, issns=issns)
    except ValueError:
        logger.error(u'Coleção de destino (%s) não existe' % args.collection_to)
    else:
        importer.run()

if __name__ == '__main__':
    main()
