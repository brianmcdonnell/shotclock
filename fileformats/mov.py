from fileformats.base import BaseFile


class MOVFile(BaseFile):
    date_format = '%a %b %d %H:%M:%S %Y\n'

    def __init__(self, path):
        super(MOVFile, self).__init__(path)
        from hachoir_parser import createParser
        from hachoir_core.cmd_line import unicodeFilename
        path = unicodeFilename(path)
        self.parser = createParser(path)
        if not self.parser:
            raise Exception("Could not parse: %s" % path)
        self._new_date = None

    def get_date(self):
        from hachoir_metadata import extractMetadata
        metadata = extractMetadata(self.parser)
        creation_date = metadata.get('creation_date')
        return creation_date

    def set_date(self, date):
        self._new_date = date

    def save_as(self, path):
        from hachoir_editor import createEditor
        editor = createEditor(self.parser)

        if self._new_date is not None:
            mv = editor['/atom[2]']['movie']
            mvhd = mv['/atom[0]']['movie_hdr']
            # old_date = mvhd['creation_date'].value
            # Set new date in metadata
            old_date = mvhd['creation_date'].value
            mvhd['creation_date'].value = old_date
            # self._new_date

        # Write out the file
        from hachoir_core.stream import FileOutputStream
        output = FileOutputStream(path)
        editor.writeInto(output)

    def close(self):
        self.parser.stream._input.close()
