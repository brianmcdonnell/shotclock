#! /usr/bin/env python
from hachoir_core import config as HachoirConfig
HachoirConfig.quiet = True


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

    renamer_parser = subparsers.add_parser('rename',
                                           help='Rename matching files to \
                                           their timestamp values.')
    renamer_parser.add_argument('--suffix', '-s', dest='suffix', default=None)
    renamer_parser.add_argument('glob', nargs='+',
                                help='Globs of files to process.')
    renamer_parser.add_argument('--exclude-original-name', '-e',
                                dest='exclude_original_name',
                                action='store_true', default=False)

    args = parser.parse_args()

    if args.subparser == 'comparedirs':
        from commands.comparedirs import CompareDirsCommand
        command = CompareDirsCommand(args.dir1, args.dir2)
    elif args.subparser == 'timeshift':
        from commands.timeshift import TimeShiftCommand
        command = TimeShiftCommand(args.hours, args.minutes)
    elif args.subparser == 'rename':
        from commands.rename import RenameCommand
        command = RenameCommand(not args.exclude_original_name, args.suffix)
    else:
        raise Exception("Unknown command")

    command.execute(args)
