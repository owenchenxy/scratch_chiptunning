#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all(thread=False)
from common.utils import start_collect, start_writer
import time
from optparse import OptionParser
import sys
import os
import shutil

def main(args):
    usage = '%prog [options]'
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-o', '--output_directory',
        action='store',
        type='string',
        metavar='OUTPUT_DIRECTORY',
        dest='output_dir',
        default='./docs',
        help='''output directory to store the scratched data'''
    )
    (options, args_left) = parser.parse_args(args=args[1:])
    if len(args_left) != 0:
        print("Error: Arguments [%s] can not be parsed." % args_left)
        sys.exit(-1)

    output_dir = options.output_dir
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    elif os.path.isfile(output_dir):
        print("Error: {0} is a existing file, please specify an empty directory for output data !".format(output_dir))
        sys.exit(-1)
    elif os.path.isdir(output_dir) and os.listdir(output_dir):
        print("Warning: {0} is not empty, please specify an empty directory for output data !".format(output_dir))
        opt = input("Enter yes to force empty the directory {0}.".format(output_dir))
        if opt == 'yes':
            shutil.rmtree(output_dir)
            os.mkdir(output_dir)
        else:
            print("Error: {0} is not empty !".format(output_dir))
            sys.exit(-1)

    writer_pool = start_writer(output_dir)
    start_collect()
    writer_pool.join()

if __name__ == "__main__":
    start_time = time.time()
    main(sys.argv)
    print(time.time() - start_time)