# coding: utf-8

import thriftpy
from thriftpy.rpc import client_context

spec = thriftpy.load('scielomanager.thrift', module_name='scielomanager_thrift')


def main():
    with client_context(spec.JournalManagerServices, '127.0.0.1', 6000) as c:
        print 'c.addArticle("ann_nlm")'
        print c.addArticle('ann_nlm')

main()

