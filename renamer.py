from sys import stderr, exit
import os
import os.path
import shutil


class Renamer(object):
    date_format = '%Y-%m-%d %H-%M-%S'
    date_compact_format = '%Y%m%d_%H%M%S'

    def __init__(self, include_filename=True, suffix=None):
        self.filename_format = '%(date)s'
        if include_filename:
            self.filename_format += ' %(filename)s'
        if suffix:
            self.filename_format += ' ' + suffix

    def process_file(self, input_path, fmtKlass, output_dir):
        # Copy the original to the output directory (only work on copy)
        input_dir, input_filename = os.path.split(input_path)
        working_path = os.path.join(output_dir, input_filename)
        shutil.copy2(input_path, working_path)
        # Get the creation date from the working copy
        fileFmt = fmtKlass(working_path)
        creation_dt = fileFmt.get_date()
        fileFmt.close()
        # Format the output filename
        output_filename = self._get_output_filename(input_filename, creation_dt)
        # Add numeric suffix to avoid name clashes
        num = 1
        while True:
            if num == 1:
                output_path = os.path.join(output_dir, output_filename)
            else:
                filename_trunc, filext = os.path.splitext(output_filename)
                filename_trunc += '(%s)' % num
                output_path = os.path.join(output_dir, filename_trunc + filext)
            # Break once we find a filename that doesn't already exist
            if not os.path.exists(output_path):
                break
            num += 1
        # Rename the working copy to the new filename
        os.rename(working_path, output_path)
        print '%s -> %s'% (input_path, output_path)

    def _get_output_filename(self, input_filename, dt):
        dir_path, filename = os.path.split(input_filename)
        filename_trunc, filext = os.path.splitext(filename)
        # Format dates
        date_str = dt.strftime(Renamer.date_format)
        date_compact_str = dt.strftime(Renamer.date_compact_format)
        # Populate templated format
        new_filename = self.filename_format % {'date': date_str,
                                               'date_compact': date_compact_str,
                                               'filename': filename_trunc}
        new_filename += filext
        return new_filename
