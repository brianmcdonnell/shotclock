from datetime import datetime

from fileformats.base import HachoirParsable


class MOVFile(HachoirParsable):

    def __init__(self, path):
        super(MOVFile, self).__init__(path)
        self._register_paths()

    @property
    def creation_date(self):
        creation_date = self.parser[self.get_path('creation_date')].value
        return creation_date

    @creation_date.setter
    def creation_date(self, value):
        assert isinstance(value, datetime)
        self.set_field('creation_date', value)

    def _register_paths(self):
        ''' Finds and registers all dates that are equivalent to
        the creation date. Used to keep all dates in sync, if creation date
        is modified. '''
        movie = self._find_atom_by_field(self.parser, 'movie')[0]
        movie_hdr = self._find_atom_by_field(movie, 'movie_hdr')[0]
        creation_date_path = movie_hdr['creation_date'].path
        self.register_field('creation_date', creation_date_path)
        self.register_field('lastmod_date', movie_hdr['lastmod_date'].path)

        tracks = self._find_atom_by_field(movie, 'track')
        for ndx, track in enumerate(tracks):
            track_hdr = self._find_atom_by_field(track, 'track_hdr')[0]
            trk_create_dt = track_hdr['creation_date'].path
            trk_lastmod_dt = track_hdr['lastmod_date'].path
            prefix = 'trk' + str(ndx) + '_'
            self.register_field(prefix + 'creation_date', trk_create_dt)
            self.register_field(prefix + 'lastmod_date', trk_lastmod_dt)

            media = self._find_atom_by_field(track, 'media')[0]
            media_hdr = self._find_atom_by_field(media, 'media_hdr')[0]
            med_create_dt = media_hdr['creation_date'].path
            med_lastmod_dt = media_hdr['lastmod_date'].path
            prefix = 'med' + str(ndx) + '_'
            self.register_field(prefix + 'creation_date', med_create_dt)
            self.register_field(prefix + 'lastmod_date', med_lastmod_dt)

    def _find_atom_by_field(self, node, field_name):
        ''' Find field by name when order is unknown/not guaranteed. '''
        found = []
        for atom in node.array('atom'):
            if field_name in atom:
                found.append(atom[field_name])

        if found:
            return found
        return None
