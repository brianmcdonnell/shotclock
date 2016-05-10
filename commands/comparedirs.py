import os
import os.path
import shutil


class CompareDirsCommand(object):

    def __init__(self, dir1, dir2):
        super(CompareDirsCommand, self).__init__()
        self._dir1 = dir1
        self._dir2 = dir2

    def execute(self, dir1, dir2):
        pass


def sha1OfFile(filepath):
    import hashlib
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()
