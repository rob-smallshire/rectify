"""Rectify.


Usage:
  rectify <input-filename> --output=<output-filename>
"""
import sys

from docopt import docopt

import rectify

from rectify.process import process_image_file


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    print(argv)
    arguments = docopt(argv=argv, version=rectify.__version__, doc=__doc__)
    print(arguments)
    input_filepath = arguments['<input-filename>']
    output_filepath = arguments['--output']
    process_image_file(input_filepath, output_filepath)

if __name__ == '__main__':
    sys.exit(main())

