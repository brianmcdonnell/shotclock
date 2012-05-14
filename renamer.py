from sys import stderr, exit

class Renamer(object):
    usage = "usage@ %prog rename [options] path"
    date_format = '%Y-%m-%d %H-%M-%S'
    filename_format = '%(date)s %(filename)s'
    output_dir = 'output'

    def __init__(self):
        import optparse
        parser = optparse.OptionParser(Renamer.usage)
        parser.add_option('--filename_format', '-f', dest='filename_format', default=Renamer.filename_format)
        self.options, self.arguments = parser.parse_args()

    def show_usage(self):
        print Renamer.usage

    def _get_output_path(self, input_path):
        import os
        dirname, filename = os.path.split(input_path)
        output_dir = os.path.join(dirname, Renamer.output_dir)
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
        self._rename_file(output_path, dt)

    def process_avi(self, input_path):
        uoutput_path, output_path = self._get_output_path(input_path)
        import shutil
        shutil.copyfile(input_path, output_path)

        #from hachoir_core.cmd_line import unicodeFilename
        #filename, realname = unicodeFilename(input_path), input_path

        # Try parsing the file
        from hachoir_parser import createParser
        parser = createParser(uoutput_path, output_path)
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

        creation_date = metadata.get('creation_date')

        # Close the file io stream
        parser.stream._input.close()
        self._rename_file(output_path, creation_date)

    def _make_output_path(self, path, dt, num=None):
        import os
        dir_path, filename = os.path.split(path)
        filename_trunc, filext = os.path.splitext(filename)
        new_filename = self.options.filename_format % {'date': dt.strftime(Renamer.date_format), 'filename': filename_trunc}
        if num:
            new_filename += ' %03d' % num
        new_filename += filext
        new_path = os.path.join(dir_path, new_filename)
        return new_path

    def _rename_file(self, input_path, dt):
        import os
        output_path = self._make_output_path(input_path, dt, None)
        num = 1
        while os.path.exists(output_path):
            num += 1
            output_path = self._make_output_path(input_path, dt, num)
        os.rename(input_path, output_path)
        print '%s -> %s'% (input_path, output_path)
