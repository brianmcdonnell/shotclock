import os


class DeDupeCommand(object):

    def __init__(self, dir):
        super(DeDupeCommand, self).__init__()
        self._dir = dir

    def execute(self, args):
        # Go though every file in the directory
        # Copy all duplicate pairs/triplets etc to subdir for review
        for path in os.listdir(self._dir):
            print path
