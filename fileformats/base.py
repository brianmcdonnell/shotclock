class HachoirParsable(object):
    def __init__(self, path):
        super(HachoirParsable, self).__init__()
        from hachoir_parser import createParser
        self.parser = createParser(unicode(path))
        if not self.parser:
            raise Exception("Could not parse: %s" % path)
        self._metadata_paths = {}
        self._field_modifications = 0

    def register_field(self, name, path):
        ''' Registers fields for read/write by name. '''
        self._metadata_paths[name] = FieldEntry(path, self.parser[path].value)

    def set_field(self, name, value):
        ''' Lazily writes a new value to a field. '''
        field = self._metadata_paths[name]
        was_modified = int(field.modified)
        field.value = value
        now_modified = int(field.modified)
        self._field_modifications += now_modified - was_modified

    def get_path(self, name):
        ''' Gets the parser path for a registered field by name. '''
        return self._metadata_paths[name].path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.parser.stream._input.close()

    def is_modified(self):
        return self._field_modifications > 0

    def save_as(self, path):
        ''' Writes the media file out with edited values to specified path. '''
        if self.is_modified():
            from hachoir_editor import createEditor
            editor = createEditor(self.parser)
            self._update_fields(editor)
            writer = editor
        else:
            writer = self.parser

        from hachoir_core.stream import FileOutputStream
        stream = FileOutputStream(path)
        writer.writeInto(stream)

    def _update_fields(self, editor):
        for name, entry in self._metadata_paths.iteritems():
            if entry.modified:
                editor[entry.path].value = entry.value


class FieldEntry(object):
    def __init__(self, path, value):
        self.path = path
        self.initial_value = value
        self.value = value

    @property
    def modified(self):
        return self.initial_value != self.value
