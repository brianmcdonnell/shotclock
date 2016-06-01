#! /usr/bin/env python
import os
import os.path
import errno

from hachoir_core import config as HachoirConfig
HachoirConfig.quiet = True


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


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

    rename_parser = subparsers.add_parser('rename',
                                          help='Rename matching files to \
                                          their timestamp values.')
    rename_parser.add_argument('--suffix', '-s', dest='suffix', default=None)
    rename_parser.add_argument('glob', nargs='+',
                               help='Globs of files to process.')
    rename_parser.add_argument('--exclude-original-name', '-e',
                               dest='exclude_original_name',
                               action='store_true', default=False)

    organize_parser = subparsers.add_parser('organize',
                                            help="Organize files into \
                                            directories.")
    organize_parser.add_argument('--config', '-s', dest='config', default=None)
    organize_parser.add_argument('glob', nargs='+',
                                 help='Globs of files to process.')

    dedupe_parser = subparsers.add_parser('dedupe',
                                          help="Identify duplicates for \
                                          review.")
    dedupe_parser.add_argument('--dir', dest='dir')
    dedupe_parser.add_argument('--hours', type=int, dest='hours', default=0)
    dedupe_parser.add_argument('--minutes', '-m',
                               type=int, dest='minutes', default=0)

    args = parser.parse_args()
    mkdir_p(args.output_dir)

    if args.subparser == 'comparedirs':
        from commands.comparedirs import CompareDirsCommand
        command = CompareDirsCommand(args.dir1, args.dir2)
    if args.subparser == 'organize':
        from commands.organize import OrganizeCommand
        command = OrganizeCommand(args.config)
    elif args.subparser == 'timeshift':
        from commands.timeshift import TimeShiftCommand
        command = TimeShiftCommand(args.hours, args.minutes)
    elif args.subparser == 'rename':
        from commands.rename import RenameCommand
        command = RenameCommand(not args.exclude_original_name, args.suffix)
    elif args.subparser == 'dedupe':
        from commands.dedupe import DeDupeCommand
        command = DeDupeCommand(args.dir, args.hours, args.minutes)
    else:
        raise Exception("Unknown command")

    command.execute(args)
