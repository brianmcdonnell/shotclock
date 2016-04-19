from fileformats.base import BaseFile

class JPEGFile(BaseFile):

    def __init__(self, path):
        super(JPEGFile, self).__init__(path)
        import pyexiv2
        self.metadata = pyexiv2.ImageMetadata(path)
        self.metadata.read()

    def get_date(self):
        dt = metadata['Exif.Image.DateTime'].value
        return dt

    def set_date(self, date):
        self.metadata['Exif.Image.DateTime'].value = date
        self.metadata['Exif.Photo.DateTimeOriginal'].value = date
        self.metadata['Exif.Photo.DateTimeDigitized'].value = date

    def save(self)
        self.metadata.write()
