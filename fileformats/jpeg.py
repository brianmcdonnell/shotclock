from fileformats.base import HachoirParsable

from datetime import datetime


class JPEGFile(HachoirParsable):
    DATE_FORMAT = '%Y:%m:%d %H:%M:%S'

    # From hachoir_parser/image/exif.py
    EXIF_TAG_CODES = {
        0x010f: "camera_manufacturer",
        0x0110: "camera_model",
        0x0132: "creation_datetime",
        0x9003: "original_datetime",
        0x9004: "digitized_datetime"
    }

    def __init__(self, path):
        super(JPEGFile, self).__init__(path)
        self._new_date = None
        self._metadata_paths = {}

        # Search ifd fields for metadata
        if "exif/content" in self.parser:
            for ifd in self.parser.array("exif/content/ifd"):
                for entry in ifd.array("entry"):
                    self._processIfdEntry(ifd, entry)

    def __hash__(self):
        pass

    def _processIfdEntry(self, ifd, entry):
        tag = entry["tag"].value
        if tag not in JPEGFile.EXIF_TAG_CODES:
            return

        key = JPEGFile.EXIF_TAG_CODES[tag]
        if "value" in entry:
            value_node = entry["value"]
        else:
            value_node = ifd["value_%s" % entry.name]
        self._metadata_paths[key] = value_node.path

    def get_date(self):
        exif_path = self._metadata_paths['creation_datetime']
        creation_date = datetime.strptime(self.parser[exif_path].value,
                                          JPEGFile.DATE_FORMAT)
        return creation_date

    def set_date(self, date):
        self._new_date = date

    def save_as(self, path):
        from hachoir_editor import createEditor
        editor = createEditor(self.parser)

        if self._new_date is not None:
            new_date_str = self._new_date.strftime(JPEGFile.DATE_FORMAT) + '\0'
            for key in ('creation_datetime',
                        'original_datetime',
                        'digitized_datetime'):
                exif_path = self._metadata_paths[key]
                editor[exif_path].value = new_date_str

        # Write out the file
        from hachoir_core.stream import FileOutputStream
        output = FileOutputStream(path)
        editor.writeInto(output)
