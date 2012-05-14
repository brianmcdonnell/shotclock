#!/usr/bin/env python
import os
import glob
import mimetypes

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

    fulltype = mimetypes.guess_type(path)
    maintype, subtype = fulltype[0].split('/')
    if (fulltype[0] == 'image/pjpeg'):
        command.process_jpeg(path)
    elif (fulltype[0] == 'video/x-msvideo'):
        command.process_avi(path)
    elif maintype == "video":
        command.process_avi(path)

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

def main():
    ''' shotclock.py (timeshift|rename) [options] path1 path2... 
    '''
    import sys
    if sys.argv[1] == 'timeshift':
        from timeshifter import TimeShifter
        command = TimeShifter()
    elif sys.argv[1] == 'rename':
        from renamer import Renamer
        command = Renamer()
    else:
        print "ShotClock photo/video organizer."
        print ""
        print "Commands:"
        print "  timeshift\t\ttranspose timestamps by specified amount"
        print "  rename   \t\trename files from metadata"
        exit(1)

    for arg in command.arguments:
        for expanded in glob.glob(arg):
            process_expanded_arg(expanded, command)

if __name__ == '__main__':
    main()

