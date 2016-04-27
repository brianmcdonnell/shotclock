from fileformats.base import BaseFile

class JPEG2File(BaseFile):

    def __init__(self, path):
        super(JPEG2File, self).__init__(path)
        from hachoir_parser import createParser
        from hachoir_core.cmd_line import unicodeFilename
        self.upath = unicodeFilename(path)
        self.parser = createParser(self.upath)
        if not self.parser:
            raise Exception("Could not parse: %s" % path)
        self._new_date = None

        import pyexiv2
        self.metadata = pyexiv2.ImageMetadata(path)
        self.metadata.read()

    def get_date(self):
        from hachoir_metadata import extractMetadata
        metadata = extractMetadata(self.parser)
        print metadata
        print ""
        for k in self.metadata:
            print k, self.metadata[k].value

        print ""
        print "--------------"


        if "exif/content" in self.parser:
            for ifd in self.parser.array("exif/content/ifd"):
                for entry in ifd.array("entry"):
                    self.processIfdEntry(ifd, entry)

        #from hachoir_parser.image.exif import ExifIFD
        #content = self.parser['/exif/content']
        #for ifd in content:
        #    if not isinstance(ifd, ExifIFD):
        #        continue
        #    for entry in ifd.array("entry"):
        #        self.processIfdEntry(ifd, entry)

        creation_date = metadata.get('creation_date')
        return creation_date

    def processIfdEntry(self, ifd, entry):
        from hachoir_metadata.jpeg import JpegMetadata
        tag = entry["tag"].value
        if tag not in JpegMetadata.EXIF_KEY:
            return

        key = JpegMetadata.EXIF_KEY[tag]
        # Read value
        if "value" in entry:
            value = entry["value"].value
        else:
            value = ifd["value_%s" % entry.name].value

        if key != 'comment':
            print entry.path, key + ':', value, type(value)
        #print ifd, entry

    def _rest_get_date(self):
        print ""
        print ifd
        for x in ifd:
            print type(x)
            print '\t', x.name, x.path, x.description, x.value
            try:
                print '\t', 'TAG', x['tag'], x['tag'].value
            except:
                pass
            #import pdb;pdb.set_trace()
        creation_date = metadata.get('creation_date')
        #dt = self.metadata['Exif.Image.DateTime'].value
        #print creation_date
        #print ""
        #print self.metadata['Exif.Image.DateTime'].value
        #print self.metadata['Exif.Photo.DateTimeOriginal'].value
        #print self.metadata['Exif.Photo.DateTimeDigitized'].value
        return creation_date

    def set_date(self, date):
        pass
        #self.metadata['Exif.Image.DateTime'].value = date
        #self.metadata['Exif.Photo.DateTimeOriginal'].value = date
        #self.metadata['Exif.Photo.DateTimeDigitized'].value = date

    def save(self):
        pass
        #self.metadata.write()
