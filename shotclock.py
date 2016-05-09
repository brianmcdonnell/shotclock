#! /usr/bin/env python

import os
import os.path

from hachoir_core import config as HachoirConfig
HachoirConfig.quiet = True


def process_file(path, command, output_dir):
    try:
        base, ext = os.path.splitext(path)
        ext = ext[1:].lower()

        from fileformats import jpeg, mov, avi
        if ext in ['jpg', 'jpeg']:
            fmtKlass = jpeg.JPEGFile
        elif ext in ['mov', 'mp4']:
            fmtKlass = mov.MOVFile
        elif ext == 'avi':
            fmtKlass = avi.AVIFile
        else:
            raise Exception("Unknown file extension: %s" % ext)

        command.process_file(path, fmtKlass, output_dir)
    except Exception:
        print "Skipping %s" % path


def process_expanded_arg(arg, command, output_dir):
    ''' We want to process lists of file and directory arguments.
        We don't want to recurse directories.
    '''
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if os.path.isfile(arg):
        process_file(arg, command, output_dir)
    elif os.path.isdir(arg):
        for p in os.listdir(arg):
            p = os.path.join(arg, p)
            if os.path.isfile(p):
                process_file(p, command, output_dir)
    else:
        print "%s not found - skipping." % arg

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', dest='output_dir', default='output')
    subparsers = parser.add_subparsers(dest='subparser',
                                       help='sub-command help')

    timeshift_parser = subparsers.add_parser('timeshift',
                                             help='Timeshift matching files \
                                             by the specified amount.')
    timeshift_parser.add_argument('--hours', type=int, dest='hours', default=0)
    timeshift_parser.add_argument('--minutes', '-m',
                                  type=int, dest='minutes', default=0)
    timeshift_parser.add_argument('glob', nargs='+',
                                  help='Globs of files to process.')

    from renamer import Renamer
    renamer_parser = subparsers.add_parser('renamer',
                                           help='Rename matching files to \
                                           their timestamp values.')
    renamer_parser.add_argument('--suffix', '-s', dest='suffix', default=None)
    renamer_parser.add_argument('glob', nargs='+',
                                help='Globs of files to process.')
    renamer_parser.add_argument('--exclude-original-name', '-e',
                                dest='exclude_original_name',
                                action='store_true', default=False)

    args = parser.parse_args()

    if args.subparser == 'timeshift':
        from timeshifter import TimeShifter
        command = TimeShifter(args.hours, args.minutes)
    elif args.subparser == 'renamer':
        command = Renamer(not args.exclude_original_name, args.suffix)
    else:
        raise Exception("Unknown command")

    import glob
    for arg in args.glob:
        for expanded in glob.glob(arg):
            if os.path.abspath(args.output_dir):
                output_dir = args.output_dir
            else:
                if os.path.isfile(expanded):
                    expanded_dirname, _ = os.path.split(expanded)
                else:
                    expanded_dirname = expanded
                output_dir = os.path.join(expanded_dirname, args.output_dir)
            output_dir = os.path.normpath(os.path.abspath(output_dir))
            process_expanded_arg(expanded, command, output_dir)
