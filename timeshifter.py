import os
import os.path
import datetime


class TimeShifter(object):
    date_format = '%a %b %d %H:%M:%S %Y\n'

    def __init__(self, hours=0, minutes=0):
        self.hours = hours
        self.minutes = minutes

    def process_file(self, input_path, fmtKlass, output_dir):
        # Get the creation date and shift it
        filefmt = fmtKlass(input_path)
        dt = filefmt.get_date()
        shifted_dt = self._shift_time(dt)

        # Update the metadata and persist to output path
        _, input_filename = os.path.split(input_path)
        output_path = os.path.join(output_dir, input_filename)
        filefmt.set_date(shifted_dt)
        filefmt.save_as(output_path)
        filefmt.close()

        print "%s: %s -> %s (h:%s m:%s)" % \
            (input_filename, dt, shifted_dt, self.hours, self.minutes)

    def _shift_time(self, input_time):
        td = datetime.timedelta(hours=self.hours, minutes=self.minutes)
        output_time = input_time + td
        return output_time
