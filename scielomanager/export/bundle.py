# coding: utf-8
import os
import tarfile
import StringIO
import tempfile
from datetime import datetime


class Bundle(object):
    def __init__(self, *args, **kwargs):
        """
        Accepts an arbitrary number of logical name - data pairs::

        b = Bundle(('arq1', 'arq1 content as str'))
        """
        self._data = dict(args)

    def _tar(self):
        """
        Generate a tarball containing the data passed at init time.

        Returns a file handler.
        """
        tmp = tempfile.NamedTemporaryFile()
        out = tarfile.open(tmp.name, 'w')

        try:
            for name, data in self._data.items():
                info = tarfile.TarInfo(name)
                info.size = len(data)
                out.addfile(info, StringIO.StringIO(data.encode('cp1252')))
        finally:
            out.close()

        tmp.seek(0)
        return tmp

    def deploy(self, target):
        data = self._tar()

        base_path = os.path.split(os.path.splitext(target)[-2])[0]
        if not os.path.exists(base_path):
            os.makedirs(base_path, 0755)

        with open(target, 'w') as f:
            f.write(data.read())


def generate_filename(prefix,
                      filetype='tar',
                      fmt='%Y%m%d-%H:%M:%S:%f'):
        """
        Generates a string to be used as the bundle filename.
        Format: <prefix>-<data-fmt>.<filetype>>
        """
        now = datetime.strftime(datetime.now(), fmt)
        return '{0}.{1}'.format('-'.join([prefix, now]), filetype)
