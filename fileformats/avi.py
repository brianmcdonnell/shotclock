from datetime import datetime

from fileformats.base import HachoirParsable


class AVIFile(HachoirParsable):
    DATE_FORMAT = '%a %b %d %H:%M:%S %Y\n'

    def __init__(self, path):
        super(AVIFile, self).__init__(path)
        self.register_field('creation_date', '/headers/datetime/text')

    @property
    def creation_date(self):
        date_field = self.parser[self.get_path('creation_date')]
        creation_date = datetime.strptime(date_field.value,
                                          AVIFile.DATE_FORMAT)
        return creation_date

    @creation_date.setter
    def creation_date(self, value):
        assert isinstance(value, datetime)
        new_date_str = value.strftime(AVIFile.DATE_FORMAT)
        new_date_str = new_date_str.upper() + '\0'
        self.set_field('creation_date', new_date_str)
