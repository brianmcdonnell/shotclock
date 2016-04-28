from datetime import datetime
from fileformats.base import BaseFile


class JPEG2File(BaseFile):
    DATE_FORMAT = '%Y:%m:%d %H:%M:%S'

    def __init__(self, path):
        super(JPEG2File, self).__init__(path)
        from hachoir_parser import createParser
        from hachoir_core.cmd_line import unicodeFilename
        self.upath = unicodeFilename(path)
        self.parser = createParser(self.upath)
        if not self.parser:
            raise Exception("Could not parse: %s" % path)

        self._metadata = {}
        for key in ('creation_date', 'camera_manufacturer', 'camera_model'):
            self._metadata[key] = None

        if "exif/content" in self.parser:
            for ifd in self.parser.array("exif/content/ifd"):
                for entry in ifd.array("entry"):
                    self._processIfdEntry(ifd, entry)

        # for k, v in self._metadata.items():
        #     print k, v

    def _processIfdEntry(self, ifd, entry):
        from hachoir_metadata.jpeg import JpegMetadata
        tag = entry["tag"].value
        if tag not in JpegMetadata.EXIF_KEY:
            return
        key = JpegMetadata.EXIF_KEY[tag]

        if key in self._metadata:
            if "value" in entry:
                value_node = entry["value"]
            else:
                value_node = ifd["value_%s" % entry.name]
            self._metadata[key] = [value_node.path, None]

    def get_date(self):
        path, value = self._metadata['creation_date']
        creation_date = datetime.strptime(self.parser[path].value,
                                          JPEG2File.DATE_FORMAT)
        return creation_date

    def set_date(self, date):
        self._metadata['creation_date'][1] = date

    def save(self):
        date_changed = self._metadata['creation_date'][1] is not None
        from hachoir_editor import createEditor
        editor = createEditor(self.parser)

        if date_changed:
            path, new_date = self._metadata['creation_date']
            node = editor[path]
            new_date_str = new_date.strftime(JPEG2File.DATE_FORMAT) + '\0'
            node.value = new_date_str

        # Write out the file
        from hachoir_core.stream import FileOutputStream
        output = FileOutputStream(u'/tmp/sample.jpg')
        editor.writeInto(output)
