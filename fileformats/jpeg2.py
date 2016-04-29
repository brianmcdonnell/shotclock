from datetime import datetime
from fileformats.base import BaseFile


class JPEG2File(BaseFile):
    DATE_FORMAT = '%Y:%m:%d %H:%M:%S'

    # From hachoir_parser/image/exif.py
    EXIF_TAG_CODES = {
        0x010f: "camera_manufacturer",
        0x0110: "camera_model",
        0x0132: "creation_datetime",
        0x9003: "original_datetime",
        0x9004: "digitized_datetime"
    }
    EXIF_TAG_NAMES = {v: k for k, v in EXIF_TAG_CODES.items()}

    def __init__(self, path):
        super(JPEG2File, self).__init__(path)
        from hachoir_parser import createParser
        from hachoir_core.cmd_line import unicodeFilename
        path = unicodeFilename(path)
        self.parser = createParser(path)
        if not self.parser:
            raise Exception("Could not parse: %s" % path)

        self._metadata = {}

        if "exif/content" in self.parser:
            for ifd in self.parser.array("exif/content/ifd"):
                for entry in ifd.array("entry"):
                    self._processIfdEntry(ifd, entry)

    def _processIfdEntry(self, ifd, entry):
        tag = entry["tag"].value
        if tag not in JPEG2File.EXIF_TAG_CODES:
            return
        print "TAG FOUND", hex(tag)

        key = JPEG2File.EXIF_TAG_CODES[tag]
        if "value" in entry:
            value_node = entry["value"]
        else:
            value_node = ifd["value_%s" % entry.name]
        self._metadata[key] = [value_node.path, None]

    def get_date(self):
        path, value = self._metadata['creation_datetime']
        creation_date = datetime.strptime(self.parser[path].value,
                                          JPEG2File.DATE_FORMAT)
        return creation_date

    def set_date(self, date):
        self._metadata['creation_datetime'][1] = date

    def save_as(self, path):
        date_changed = self._metadata['creation_datetime'][1] is not None
        from hachoir_editor import createEditor
        editor = createEditor(self.parser)

        if date_changed:
            new_date = self._metadata['creation_datetime'][1]
            new_date_str = new_date.strftime(JPEG2File.DATE_FORMAT) + '\0'
            for key in ('creation_datetime',
                        'original_datetime',
                        'digitized_datetime'):
                path = self._metadata[key][0]
                editor[path].value = new_date_str

        # Write out the file
        from hachoir_core.stream import FileOutputStream
        output = FileOutputStream(path)
        editor.writeInto(output)

    def close(self):
        self.parser.stream._input.close()
