from fileformats.base import BaseFile


class MOVFile(BaseFile):

    def __init__(self, path):
        super(MOVFile, self).__init__()
        from hachoir_parser import createParser
        self.parser = createParser(unicode(path))
        if not self.parser:
            raise Exception("Could not parse: %s" % path)

        self._new_date = None
        self._creation_date_path, self._date_paths = self._find_date_paths()

    def get_date(self):
        creation_date = self.parser[self._creation_date_path].value
        return creation_date

    def set_date(self, date):
        self._new_date = date

    def save_as(self, path):
        from hachoir_editor import createEditor
        editor = createEditor(self.parser)

        if self._new_date is not None:
            for exif_path in self._date_paths:
                field = editor[exif_path]
                field.value = self._new_date

        # Write out the file
        from hachoir_core.stream import FileOutputStream
        output = FileOutputStream(path)
        editor.writeInto(output)

    def _find_atom_by_field(self, node, field_name):
        found = []
        for atom in node.array('atom'):
            if field_name in atom:
                found.append(atom[field_name])

        if found:
            return found
        return None

    def _find_date_paths(self):
        paths = []

        movie = self._find_atom_by_field(self.parser, 'movie')[0]
        movie_hdr = self._find_atom_by_field(movie, 'movie_hdr')[0]
        creation_date_path = movie_hdr['creation_date'].path
        paths.append(creation_date_path)
        paths.append(movie_hdr['lastmod_date'].path)

        tracks = self._find_atom_by_field(movie, 'track')
        for track in tracks:
            track_hdr = self._find_atom_by_field(track, 'track_hdr')[0]
            paths.append(track_hdr['creation_date'].path)
            paths.append(track_hdr['lastmod_date'].path)

            media = self._find_atom_by_field(track, 'media')[0]
            media_hdr = self._find_atom_by_field(media, 'media_hdr')[0]
            paths.append(media_hdr['creation_date'].path)
            paths.append(media_hdr['lastmod_date'].path)

        return creation_date_path, paths

    def close(self):
        self.parser.stream._input.close()
