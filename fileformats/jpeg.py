from datetime import datetime

from fileformats.base import HachoirParsable


class JPEGFile(HachoirParsable):
    DATE_FORMAT = '%Y:%m:%d %H:%M:%S'

    # From hachoir_parser/image/exif.py
    EXIF_TAG_CODES = {
        0x010f: "camera_manufacturer",
        0x0110: "camera_model",
        0x0132: "creation_datetime",
        0x0202: "jpeg_bytes",
        0x9003: "original_datetime",
        0x9004: "digitized_datetime",
        0x9201: "shutter_speed",
        0x9202: "aperture",
        0x9203: "brightness",
        0x920A: "focal_length1",
        0xA420: "unique_image_id",
        0xA405: "focal_length2",
    }

    def __init__(self, path):
        super(JPEGFile, self).__init__(path)
        self._register_fields()

    def _register_fields(self):
        # Search ifd fields for metadata
        if "exif/content" in self.parser:
            for ifd in self.parser.array("exif/content/ifd"):
                for entry in ifd.array("entry"):
                    self._processIfdEntry(ifd, entry)

    def _processIfdEntry(self, ifd, entry):
        tag = entry["tag"].value
        if tag not in JPEGFile.EXIF_TAG_CODES:
            return

        name = JPEGFile.EXIF_TAG_CODES[tag]
        if "value" in entry:
            value_node = entry["value"]
        else:
            value_node = ifd["value_%s" % entry.name]
        self.register_field(name, value_node.path)

    @property
    def creation_date(self):
        date_str = self.parser[self.get_path('creation_datetime')].value
        return datetime.strptime(date_str, JPEGFile.DATE_FORMAT)

    @creation_date.setter
    def creation_date(self, value):
        assert isinstance(value, datetime)
        date_str = value.strftime(JPEGFile.DATE_FORMAT) + '\0'
        self.set_field('creation_datetime', date_str)
