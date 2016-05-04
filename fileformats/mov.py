from fileformats.base import BaseFile


class MOVFile(BaseFile):
    date_format = '%a %b %d %H:%M:%S %Y\n'

    def __init__(self, path):
        super(MOVFile, self).__init__()
        from hachoir_parser import createParser
        from hachoir_core.cmd_line import unicodeFilename
        path = unicodeFilename(path)
        self.parser = createParser(path)
        if not self.parser:
            raise Exception("Could not parse: %s" % path)
        self._new_date = None
        self.inspect()

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
            # old_date = mvhd['creation_date'].value
            # mvhd['creation_date'].value = old_date
            mvhd['creation_date'].value = self._new_date
            # self._new_date

        # Write out the file
        from hachoir_core.stream import FileOutputStream
        output = FileOutputStream(path)
        editor.writeInto(output)

    def _find_atom_by_field(self, node, field_name):
        for atom in node.array('atom'):
            print [x for x in atom._fields.iterkeys()]
            if field_name in atom:
                 # print "Found:", field_name
                return atom[field_name]
        # print "Not found:", field_name
        return None

    def inspect(self):
        movie = self._find_atom_by_field(self.parser, 'movie')
        movie_hdr = self._find_atom_by_field(movie, 'movie_hdr')
        # import pdb;pdb.set_trace()
        print movie_hdr['creation_date']
        print movie_hdr['lastmod_date']

        print "--- track ---"
        track = self._find_atom_by_field(movie, 'track')
        track_hdr = self._find_atom_by_field(track, 'track_hdr')
        print track_hdr['creation_date']
        print track_hdr['lastmod_date']

        print "--- media ---"
        media = self._find_atom_by_field(track, 'media')
        media_hdr = self._find_atom_by_field(media, 'media_hdr')
        print media_hdr['creation_date']
        print media_hdr['lastmod_date']

    def close(self):
        self.parser.stream._input.close()
