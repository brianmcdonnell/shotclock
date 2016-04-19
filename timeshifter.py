import os
import os.path
from sys import stderr, exit
import datetime

class TimeShifter(object):
    date_format = '%a %b %d %H:%M:%S %Y\n'

    def __init__(self, hours=0, minutes=0):
        self.hours = hours
        self.minutes = minutes

    def process_file(self, input_path, fmtKlass, output_dir):
        # Copy the original to the output directory (only work on copy)
        input_dir, input_filename = os.path.split(input_path)
        output_path = os.path.join(output_dir, input_filename)
        import shutil
        shutil.copyfile(input_path, output_path)
        # Get the creation date and shift it
        filefmt = fmtKlass(output_path)
        dt = filefmt.get_date()
        shifted_dt = self._shift_time(dt)
        # Update the output file
        filefmt.set_date(shifted_dt)
        filefmt.save()
        filefmt.close()

    def _shift_time(self, input_time):
        td = datetime.timedelta(hours=self.hours, minutes=self.minutes)
        output_time = input_time + td
        print "%s -> %s (h:%s m:%s)" % (input_time, output_time, self.hours, self.minutes)
        return output_time
