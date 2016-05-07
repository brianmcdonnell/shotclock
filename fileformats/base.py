class HachoirParsable(object):

    def __init__(self, path):
        super(HachoirParsable, self).__init__()
        from hachoir_parser import createParser
        self.parser = createParser(unicode(path))
        if not self.parser:
            raise Exception("Could not parse: %s" % path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.parser.stream._input.close()
