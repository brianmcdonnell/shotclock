import os
import os.path
import datetime

from filecommand import FileCommand
from fileformats import get_metadata_handler


class TimeShiftCommand(FileCommand):
    name = "timeshift"

    @classmethod
    def add_parse_args(cls, subparsers):
        parser = subparsers.add_parser(cls.name,
                                       help='Timeshift matching files \
                                       by the specified amount.')
        parser.add_argument('--hours', type=int, dest='hours', default=0)
        parser.add_argument('--minutes', '-m',
                            type=int, dest='minutes', default=0)
        parser.add_argument('glob', nargs='+',
                            help='Globs of files to process.')

    def __init__(self, args):
        super(TimeShiftCommand, self).__init__()
        self.hours = args.hours
        self.minutes = args.minutes

    def process_file(self, input_path, output_dir):
        # Get the creation date and shift it
        fmt_klass = get_metadata_handler(input_path)
        with fmt_klass(input_path) as file_fmt:
            dt = file_fmt.creation_date
            shifted_dt = self._shift_time(dt)

            # Update the metadata and persist to output path
            _, input_filename = os.path.split(input_path)
            output_path = os.path.join(output_dir, input_filename)
            file_fmt.creation_date = shifted_dt
            file_fmt.save_as(unicode(output_path))

            print "%s: %s -> %s (h:%s m:%s)" % \
                (input_filename, dt, shifted_dt, self.hours, self.minutes)

    def _shift_time(self, input_time):
        td = datetime.timedelta(hours=self.hours, minutes=self.minutes)
        output_time = input_time + td
        return output_time
