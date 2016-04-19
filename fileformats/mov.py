from fileformats.base import BaseFile

class AVIFile(BaseFile):
    date_format = '%a %b %d %H:%M:%S %Y\n'

    def __init__(self, path):
        super(AVIFile, self).__init__(path)
        from hachoir_parser import createParser
        from hachoir_core.cmd_line import unicodeFilename
        self.upath = unicodeFilename(path)
        self.parser = createParser(path, self.upath)
        if not self.parser:
            raise Exception("Could not parse: %s" % path)
        self._new_date = None

    def get_date(self):
        from hachoir_metadata import extractMetadata
        metadata = extractMetadata(parser)
        creation_date = metadata.get('creation_date')
        return creation_date

    def set_date(self, date):
        self._new_date = date

    def save(self):
        if self._new_date is not None:
            from hachoir_editor import createEditor
            editor = createEditor(self.parser)
            mv = editor['/atom[2]']['movie']
            mvhd = mv['/atom[0]']['movie_hdr']
            # old_date = mvhd['creation_date'].value
            # Set new date in metadata
            mvhd['creation_date'] = self._new_date
            # Write out the file
            from hachoir_core.stream import FileOutputStream
            output = FileOutputStream(self.upath, self.path)
            editor.writeInto(output)

    def close(self):
        # Close the file io stream
        parser.stream._input.close()
