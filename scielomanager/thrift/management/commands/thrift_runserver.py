# coding: utf-8

import sys
from django.core.management.base import BaseCommand
from thrift import server


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        server.serve()
