class CompareDirsCommand(object):
    name = "compare-dirs"

    def __init__(self, args):
        super(CompareDirsCommand, self).__init__()
        self._dir1 = args.dir1
        self._dir2 = args.dir2

    @classmethod
    def add_parse_args(cls, subparsers):
        subparsers.add_parser(cls.name,
                              help='Highlight differences \
                                    between dirs.')

    def execute(self):
        pass


def sha1OfFile(filepath):
    import hashlib
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()
