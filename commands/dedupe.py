import os
import os.path
from datetime import timedelta
from collections import namedtuple
import shutil

from fileformats import get_metadata_handler


File = namedtuple('File', ['filename', 'byte_size', 'creation_date'])


class DeDupeCommand(object):

    def __init__(self, args):
        super(DeDupeCommand, self).__init__()
        self._dir = args.dir
        td = timedelta(hours=args.hours, minutes=args.mins)
        self._tolerance = td.total_seconds()
        self._tolerance = abs(self._tolerance)
        print "TOLERANCE (secs)", self._tolerance

    def _get_files(self):
        files = []
        for filename in os.listdir(self._dir):
            try:
                path = os.path.join(self._dir, filename)
                # Get each file's byte size and metadata creation date
                # If same size and within date tolerance, consider them
                # duplicates
                byte_size = os.path.getsize(path)
                fmt_klass = get_metadata_handler(path)
                with fmt_klass(path) as file_fmt:
                    creation_dt = file_fmt.creation_date
                files.append(File(filename, byte_size, creation_dt))
            except Exception as e:
                print e
                print "skipping", path
        print "SORTING %s files" % len(files)
        files = sorted(files, lambda a, b: a.byte_size < b.byte_size)
        return files

    def _get_dupes(self, files):
        dupe_pairs = []
        dupes = set()
        if files:
            f1 = files.pop(0)
            for f2 in files:
                # print f2.filename
                if f1.byte_size == f2.byte_size:
                    if self._is_duplicate(f1, f2):
                        dupe_pairs.append((f1, f2))
                        dupes.add(f2.filename)
                f1 = f2

        print ""
        print "DUPE PAIRS", len(dupes)
        for f1, f2 in dupe_pairs:
            print f1.filename, f2.filename
        return dupes

    def _is_duplicate(self, file1, file2):
        if file1.byte_size == file2.byte_size:
            td = file1.creation_date - file2.creation_date
            return abs(td.total_seconds()) <= self._tolerance

    def execute(self, args):
        files = self._get_files()
        dupes = self._get_dupes(files)

        existing_files = set([f for f in os.listdir(args.output_dir)])

        source_files = sorted([f for f in os.listdir(self._dir)])
        for filename in source_files:
            if filename in existing_files:
                continue

            print "Considering", filename
            if filename not in dupes:
                print "Copying", filename
                src_path = os.path.join(self._dir, filename)
                dst_path = os.path.join(args.output_dir, filename)
                shutil.copy2(src_path, dst_path)
                print "Copied", filename
