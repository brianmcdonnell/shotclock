import os
import os.path
from collections import namedtuple
from datetime import datetime
import csv

from filecommand import FileCommand
from fileformats import get_metadata_handler


Rule = namedtuple('Rule', ['after_date', 'before_date', 'format'])

class Rule(object):
    def __init__(self, path_format, date_range):
        self.path_format = path_format
        self.from_date = date_range[0]
        self.to_date = date_range[1]

    def is_match(self, file_date):
        if self.from_date is None and self.to_date is None:
            return True
        return self.from_date <= file_date < self.to_date


class OrganizeCommand(FileCommand):
    name = "organize"
    date_formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S']

    @classmethod
    def add_parse_args(cls, subparsers):
        parser = subparsers.add_parser(cls.name,
                                       help="Organize files into directories.")
        parser.add_argument('--config', '-s', dest='config', default=None)
        parser.add_argument('glob', nargs='+', help='Globs to process.')

    def __init__(self, args):
        super(OrganizeCommand, self).__init__()
        self._rules = []

        if args.config:
            with open(args.config, 'r') as f:
                csvreader = csv.DictReader(f)
                for row in csvreader:
                    path_format = row['path_format']
                    from_date = _parse_date(row['from_date']) if row['from_date'] else None
                    to_date = _parse_date(row['to_date']) if row['to_date'] else None
                    self._rules.append(Rule(path_format, (from_date, to_date)))


    def process_file(self, input_path, output_dir):
        fmt_klass = get_metadata_handler(input_path)
        with fmt_klass(input_path) as file_fmt:
            creation_date = file_fmt.creation_date

        rule = self._get_matching_rule(creation_date)

        metadata = {}
        directives = ('Y', 'm', 'B', 'H', 'M', 'S')
        for d in directives:
            metadata[d] = datetime.strftime(creation_date, '%' + d)
        target_path = rule.path_format % metadata

        _, filename = os.path.split(input_path)
        output_dir = os.path.join(output_dir, target_path)
        from shotclock import mkdir_p
        mkdir_p(output_dir)
        output_path = os.path.join(output_dir, filename)

        import shutil
        # shutil.copy2(input_path, output_path)
        print '%s -> %s' % (input_path, output_path)

    def _get_matching_rule(self, file_date):
        for rule in self._rules:
            if rule.is_match(file_date):
                return rule
        raise Exception('No matching rule & no default rule')

def _parse_date(str):
        dt = None
        for fmt in OrganizeCommand.date_formats:
            try:
                dt = datetime.strptime(str, fmt)
            except:
                pass
        if dt is None:
            raise ValueError("Invalid date '%s'. Valid formats: %s" %
                             (str, OrganizeCommand.date_formats))
        return dt
