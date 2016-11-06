import os
import os.path
import shutil


class CompareDirsCommand(object):

    def __init__(self, args):
        super(CompareDirsCommand, self).__init__()
        self._dir1 = args.dir1
        self._dir2 = args.dir2

    def execute(self):
        pass


def sha1OfFile(filepath):
    import hashlib
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()
