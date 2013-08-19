#! /usr/bin/env python

import os

def create_backup(input_path):
    dir_path, filename = os.path.split(input_path)
    bkp_dir = os.path.join(dir_path, 'bkp')

    # Don't proceed unless we can backup the files
    if os.path.isfile(bkp_dir):
        raise Exception("File exists at backup dir location.")
    if not os.path.exists(bkp_dir):
        os.makedirs(bkp_dir)

    # Backup the file
    bkp_path = os.path.join(bkp_dir, filename)
    if os.path.isfile(bkp_path):
        raise Exception("Backup file already exists.  Will not overwrite.")
    import shutil
    shutil.copyfile(input_path, bkp_path)

def process_file(path, command):
    # Backup the file before it's processed
    #create_backup(path)

    import mimetypes
    fulltype = mimetypes.guess_type(path)
    maintype, subtype = fulltype[0].split('/')
    if fulltype[0] in ['image/jpeg', 'image/pjpeg']:
        command.process_jpeg(path)
    elif fulltype[0] == 'video/x-msvideo':
        command.process_avi(path)
    elif maintype == "video":
        command.process_avi(path)
    else:
        raise Exception("Unknown filetype: %s" % fulltype[0])

def process_expanded_arg(arg, command):
    ''' We want to process lists of file and directory arguments.
        We don't want to recurse directories.
    '''
    if os.path.isfile(arg):
        process_file(arg, command)
    elif os.path.isdir(arg):
        for p in os.listdir(arg):
            p = os.path.join(arg, p)
            if os.path.isfile(p):
                process_file(p, command)
    else:
        print "%s not found - skipping." % arg

def main():
    import argparse
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser', help='sub-command help')

    timeshift_parser = subparsers.add_parser('timeshift', help='Timeshift matching files by the specified amount.')
    timeshift_parser.add_argument('--hours', type=int, dest='hours', default=None)
    timeshift_parser.add_argument('--minutes', '-m', type=int, dest='minutes', default=None)
    timeshift_parser.add_argument('glob', nargs='+', help='Globs of files to process.')

    from renamer import Renamer
    renamer_parser = subparsers.add_parser('renamer', help='Rename matching files to their timestamp values.')
    renamer_parser.add_argument('--format', '-f', default=Renamer.filename_format)
    renamer_parser.add_argument('glob', nargs='+', help='Globs of files to process.')

    args = parser.parse_args()

    if args.subparser == 'timeshift':
        from timeshifter import TimeShifter
        command = TimeShifter(args.hours, args.minutes)
    elif args.subparser == 'renamer':
        command = Renamer(args.format)
    else:
        raise Exception("Unknown command")

    import glob
    for arg in args.glob:
        for expanded in glob.glob(arg):
            process_expanded_arg(expanded, command)

if __name__ == '__main__':
    print "ASD"
    main()

