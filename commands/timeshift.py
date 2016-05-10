import os
import os.path
import datetime

from filecommand import FileCommand


class TimeShiftCommand(FileCommand):

    def __init__(self, hours=0, minutes=0):
        super(TimeShiftCommand, self).__init__()
        self.hours = hours
        self.minutes = minutes

    def process_file(self, input_path, output_dir):
        # Get the creation date and shift it
        fmt_klass = self._get_metadata_handler(input_path)
        with fmt_klass(input_path) as file_fmt:
            dt = file_fmt.get_date()
            shifted_dt = self._shift_time(dt)

            # Update the metadata and persist to output path
            _, input_filename = os.path.split(input_path)
            output_path = os.path.join(output_dir, input_filename)
            file_fmt.set_date(shifted_dt)
            file_fmt.save_as(unicode(output_path))

            print "%s: %s -> %s (h:%s m:%s)" % \
                (input_filename, dt, shifted_dt, self.hours, self.minutes)

    def _shift_time(self, input_time):
        td = datetime.timedelta(hours=self.hours, minutes=self.minutes)
        output_time = input_time + td
        return output_time
