#!/usr/bin/python
#coding:utf-8

import os
import json
import shutil
import urllib
import tarfile
import urllib2
import tempfile
import argparse

import config


def save_bundle_tar(file_name, data, path=""):
    try:
        bundle = open(os.path.join(path, file_name + '.tar'), "w")
        bundle.write(data.read())
        bundle.close()
    except IOError, e:
        print 'IO Error:', e


def extract_tar(file_name, path=""):
    try:
        tarfile.open(os.path.join(path, file_name + '.tar'), 'r').extract(file_name + '.id', path)
        return os.path.join(path, file_name + '.id')
    except IOError, e:
        print "IOError:", e


def fetch_url(url, params=None):
    try:
        return urllib2.urlopen(url + "?%s" % params if params else url)
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code


def isis_exec(cmd):
    try:
        os.system(cmd)
    except OSError, e:
        print "OSError:", e


def main():

    parser = argparse.ArgumentParser(
        description='Script to get metadata from SciELO Manager \
            and generate databases for Title Manager')

    parser.add_argument('-c', '--collection',
        help='the collection name to get metadata', required=True)
    parser.add_argument('-o', '--output',
        help='the output path to isis databases', required=True)

    args = parser.parse_args()

    try:
        tmp_dir = tempfile.mkdtemp()
        print "Generated process directory: " + tmp_dir
    except OSError, e:
        print "OSError:", e

    for database in config.DATABASES:
        print "Get metadata from database: " + database.upper() + " on collection " \
            + args.collection.upper() + "..."
        params = urllib.urlencode({'collection': args.collection})
        resource_response = fetch_url(config.DELOREAN_URL + database, params)
        bundle_dict = json.loads(resource_response.read())
        bundle = fetch_url(bundle_dict['expected_bundle_url'])

        print "Generate tar file..."
        save_bundle_tar(database, bundle, tmp_dir)

        print "Extract tar file and generate " + database + " id file."
        database_id = extract_tar(database, tmp_dir)

        print "Generate isis database: " + database
        isis_exec(config.ISIS_PATH + 'id2i ' + database_id + ' create/app=' \
            + os.path.join(args.output, database, database))

        print "Generate isis index using fst: " + config.DATABASE_FST[database]
        isis_exec(config.ISIS_PATH + 'mx ' + os.path.join(args.output, database, database) \
            + ' fst=@' + config.DATABASE_FST[database] + '.fst fullinv/ansi=' \
            + os.path.join(args.output, database, config.DATABASE_FST[database]) + ' -all now')

    print "Deleting temp directory: " + tmp_dir
    shutil.rmtree(tmp_dir)
    print "Finish process."

if __name__ == "__main__":
    main()
