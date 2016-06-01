import os
from fileformats import get_metadata_handler

class FileCommand(object):

    def execute(self, args):
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
                    output_dir = os.path.join(expanded_dirname,
                                              args.output_dir)
                output_dir = os.path.normpath(os.path.abspath(output_dir))
                self._process_expanded_arg(expanded, output_dir)

    def _process_expanded_arg(self, arg, output_dir):
        ''' We want to process lists of file and directory arguments.
            We don't want to recurse directories.
        '''
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if os.path.isfile(arg):
            self._try_process_file(arg, output_dir)
        elif os.path.isdir(arg):
            for path in os.listdir(arg):
                path = os.path.join(arg, path)
                if os.path.isfile(path):
                    self._try_process_file(path, output_dir)
        else:
            print "%s not found - skipping." % arg

    def _try_process_file(self, path, output_dir):
        try:
            self.process_file(path, output_dir)
        except Exception as e:
            print "Skipping %s" % path, e
            raise
