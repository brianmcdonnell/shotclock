from sys import stderr, exit
import datetime

class TimeShifter(object):
    date_format = '%a %b %d %H:%M:%S %Y\n'
    output_dir = 'output'

    def __init__(self, hours=0, minutes=0):
        self.hours = hours
        self.minutes = minutes

    def _get_output_path(self, input_path):
        import os
        dirname, filename = os.path.split(input_path)
        output_dir = os.path.join(dirname, TimeShifter.output_dir)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, filename)
        return unicode(output_path), str(output_path)

    def process_jpeg(self, input_path):
        uoutput_path, output_path = self._get_output_path(input_path)
        import shutil
        shutil.copyfile(input_path, output_path)

        import pyexiv2
        metadata = pyexiv2.ImageMetadata(output_path)
        metadata.read()
        dt = metadata['Exif.Image.DateTime'].value

        # Replace exif dates with shifted date
        shifted_dt = self._shift_time(dt)
        metadata['Exif.Image.DateTime'].value = shifted_dt
        metadata['Exif.Photo.DateTimeOriginal'].value = shifted_dt
        metadata['Exif.Photo.DateTimeDigitized'].value = shifted_dt

        # Write output file
        metadata.write()

    def process_avi(self, input_path):
        # Try parsing the file
        from hachoir_parser import createParser
        from hachoir_core.cmd_line import unicodeFilename
        uinput_path = unicodeFilename(input_path)
        parser = createParser(uinput_path, input_path)
        if not parser:
            print >> stderr, "Unable to parse file"
            exit(1)

        # Extract metadata from the file
        from hachoir_metadata import extractMetadata
        from hachoir_core.error import HachoirError
        try:
            metadata = extractMetadata(parser)
        except HachoirError, err:
            print >> stderr, "Metadata extraction error: %s" % unicode(err)
            metadata = None
        if not metadata:
            print >> stderr, "Unable to extract metadata"
            exit(1)

        # Can rewrite the datetime here easily if the new datetime string length
        # is the same as the old datetime string length.
        # If the length were to change, we'd have to update various chunk length values
        # e.g. file size, header size and datetime size
        from hachoir_editor import createEditor
        editor = createEditor(parser)
        headers_fieldset = editor['headers']
        datetime_fieldset = headers_fieldset['datetime']

        # Chop off the last character
        original_datetime_str = datetime_fieldset['text'].value
        #original_datetime_str = original_datetime_str[:-1]
        original_datetime = datetime.datetime.strptime(original_datetime_str, TimeShifter.date_format)

        # Shift time as specified in args
        shifted_time = self._shift_time(original_datetime)
        shifted_time_str = shifted_time.strftime(TimeShifter.date_format).upper()
        shifted_time_str += '\0'

        # Modify the metadata fields
        datetime_fieldset['text'].value = shifted_time_str
        datetime_fieldset['size'].value = len(shifted_time_str)

        # Write out the file
        uoutput_path, output_path = self._get_output_path(input_path)
        from hachoir_core.stream import FileOutputStream
        output = FileOutputStream(uoutput_path, output_path)
        editor.writeInto(output)

        # Close the file io stream
        parser.stream._input.close()

    def _shift_time(self, input_time):
        td = datetime.timedelta(hours=self.hours, minutes=self.minutes)
        output_time = input_time + td
        print "%s -> %s (h:%s m:%s)" % (input_time, output_time, self.hours, self.minutes)
        return output_time
