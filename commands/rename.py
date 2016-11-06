import os
import os.path
import shutil

from filecommand import FileCommand
from fileformats import get_metadata_handler


class RenameCommand(FileCommand):
    date_format = '%Y-%m-%d %H-%M-%S'

    def __init__(self, args):
        super(RenameCommand, self).__init__()
        include_filename = not args.exclude_original_name
        suffix = args.suffix
        self.filename_format = '%(date)s'
        if include_filename:
            self.filename_format += ' %(filename)s'
        if suffix:
            self.filename_format += ' ' + suffix

    def process_file(self, input_path, output_dir):
        # Get the creation date from the working copy
        fmt_klass = get_metadata_handler(input_path)
        with fmt_klass(input_path) as file_fmt:
            creation_dt = file_fmt.creation_date

        # Format the output path
        _, input_filename = os.path.split(input_path)
        output_filename = self._get_output_filename(input_filename,
                                                    creation_dt)
        output_filename = self._get_unique_filename(output_dir,
                                                    output_filename)
        output_path = os.path.join(output_dir, output_filename)

        # Rename the working copy to the new filename
        shutil.copy2(input_path, output_path)
        print '%s -> %s' % (input_path, output_path)

    def _get_output_filename(self, input_filename, dt):
        dir_path, filename = os.path.split(input_filename)
        filename_trunc, filext = os.path.splitext(filename)
        # Format dates
        date_str = dt.strftime(RenameCommand.date_format)
        # Populate templated format
        template_vars = {'date': date_str,
                         'filename': filename_trunc}
        new_filename = self.filename_format % template_vars
        new_filename += filext
        return new_filename

    def _get_unique_filename(self, output_dir, filename):
        # Add numeric suffix to avoid name clashes
        filename_trunc, file_ext = os.path.splitext(filename)
        num = 1
        while True:
            if num == 1:
                output_filename = filename
                output_path = os.path.join(output_dir, output_filename)
            else:
                output_filename = filename_trunc + '(%s)' % num
                output_filename += file_ext
                output_path = os.path.join(output_dir, output_filename)
            # Break once we find a filename that doesn't already exist
            if not os.path.exists(output_path):
                break
            num += 1

        return output_path
