from fileformats.base import BaseFile

from datetime import datetime


class AVIFile(BaseFile):
    DATE_FORMAT = '%a %b %d %H:%M:%S %Y\n'

    def __init__(self, path):
        super(AVIFile, self).__init__()
        from hachoir_parser import createParser
        self.parser = createParser(unicode(path))
        if not self.parser:
            raise Exception("Could not parse: %s" % path)

        self._date_path = '/headers/datetime/text'
        self._new_date = None

    def get_date(self):
        date_field = self.parser[self._date_path]
        creation_date = datetime.strptime(date_field.value,
                                          AVIFile.DATE_FORMAT)
        return creation_date

    def set_date(self, date):
        self._new_date = date

    def save_as(self, path):
        from hachoir_editor import createEditor
        editor = createEditor(self.parser)

        if self._new_date is not None:
            new_date_str = self._new_date.strftime(AVIFile.DATE_FORMAT)
            new_date_str = new_date_str.upper() + '\0'

            # Modify the metadata fields
            date_field = editor[self._date_path]
            date_field.value = new_date_str

        # Write out the file
        from hachoir_core.stream import FileOutputStream
        output = FileOutputStream(path)
        editor.writeInto(output)

    def close(self):
        self.parser.stream._input.close()
