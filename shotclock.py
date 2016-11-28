#! /usr/bin/env python
import os
import os.path
import errno

from hachoir_core import config as HachoirConfig
HachoirConfig.quiet = True

from commands.organize import OrganizeCommand
from commands.timeshift import TimeShiftCommand
from commands.rename import RenameCommand


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
    subparsers = parser.add_subparsers(dest='command_name')

    command_list = [TimeShiftCommand,
                    RenameCommand,
                    OrganizeCommand]

    command_map = {}
    for klass in command_list:
        command_map[klass.name] = klass
        klass.add_parse_args(subparsers)

    args = parser.parse_args()
    mkdir_p(args.output_dir)

    klass = command_map.get(args.command_name, None)
    if klass:
        command = klass(args)
    else:
        raise Exception("Unknown command")

    command.execute(args)
