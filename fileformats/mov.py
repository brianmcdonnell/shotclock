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
        self._date_paths = self._find_date_paths()

    def get_date(self):
        path = self._date_paths['creation_date']
        creation_date = self.parser[path].value
        return creation_date

    def set_date(self, date):
        self._new_date = date

    def save_as(self, path):
        from hachoir_editor import createEditor
        editor = createEditor(self.parser)

        if self._new_date is not None:
            for field_name, exif_path in self._date_paths.iteritems():
                field = editor[exif_path]
                field.value = self._new_date
                print exif_path, field.value

        # Write out the file
        from hachoir_core.stream import FileOutputStream
        output = FileOutputStream(path)
        editor.writeInto(output)

    def _find_atom_by_field(self, node, field_name):
        found = []
        for atom in node.array('atom'):
            # print [x for x in atom._fields.iterkeys()]
            if field_name in atom:
                 # print "Found:", field_name
                found.append(atom[field_name])

        # print "Not found:", field_name
        if found:
            print field_name, len(found)
            return found
        return None

    def _find_date_paths(self):
        paths = {}

        movie = self._find_atom_by_field(self.parser, 'movie')[0]
        movie_hdr = self._find_atom_by_field(movie, 'movie_hdr')[0]
        # import pdb;pdb.set_trace()
        paths['creation_date'] = movie_hdr['creation_date'].path
        paths['modified_date'] = movie_hdr['lastmod_date'].path

        tracks = self._find_atom_by_field(movie, 'track')
        for track in tracks:
            track_hdr = self._find_atom_by_field(track, 'track_hdr')[0]
            paths['track_creation_date'] = track_hdr['creation_date'].path
            paths['track_modified_date'] = track_hdr['lastmod_date'].path

            media = self._find_atom_by_field(track, 'media')[0]
            media_hdr = self._find_atom_by_field(media, 'media_hdr')[0]
            paths['media_creation_date'] = media_hdr['creation_date'].path
            paths['media_modified_date'] = media_hdr['lastmod_date'].path

        print "   "

        for field_name, exif_path in paths.iteritems():
            field = self.parser[exif_path]
            print "INSPECT", exif_path, field.value


        return paths

    def close(self):
        self.parser.stream._input.close()
