import os

from django.conf import settings
import thriftpy


HERE = os.path.dirname(os.path.abspath(__file__))


# data transfer objects and services build at runtime
spec = thriftpy.load(os.path.join(HERE, 'scielomanager.thrift'), module_name='scielomanager_thrift')

