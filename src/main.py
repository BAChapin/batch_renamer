# ****************************** Developer Notes ******************************
# Goal: Build a command line tool that will allow me to rename a directory of
# scanned images. For additional functionality, I want the following pieces
# of functionality:
# 1. DIRECTORY: This is a required argument.
#   - Convert a string into an absolute directory path. Should enable drag and
#     drop functionality from the terminal
# 2. RENAME_SCHEME: '-n'
#   - DEFAULT: Date of running software, 'YYYY.mm.dd_####'
#   - If given a scheme, 'NAMESCHEME_####'
# 3. TYPE: '-t'
#   - DEFAULT: '.*'
#   - Whatever is passed in, the software will only rename those files. '.jpg'
#     will only change the names of files that are 'jpg', which means it will
#     exclude files with any other extension, including 'jpeg'
# 4. VERBOSE: '-v'
#   - False by default. If True, it will print the name of the file being
#     changed and what it has been named to. 'scan.pdf -> document_0012.pdf'
# *****************************************************************************

import argparse
import datetime
import glob
from os import listdir, rename
from os.path import isdir, exists

DESCRIPTION = 'Software to make renaming batches of files easier. By ' \
    'supplying a few simple parameters we will take care of renaming an ' \
    'entire directory of files.'

def arg_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('dir')

    parser.add_argument(
        '-s',
        '--scheme',
        type=str,
        required=False,
        dest='name'
    )

    parser.add_argument(
        '-t',
        '--type',
        type=str,
        required=False,
        dest='type'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        required=False,
        default=False,
        action='store_true',
        dest='verbose'
    )

    args = parser.parse_args()
    main(args)

def main(args):
    scheme = args.name
    type = args.type
    verbose = args.verbose
    dir = args.dir
    renamed_count = 0

    # Set 'scheme'
    #   - if not passed in as param, get default
    if scheme is None:
        scheme = get_scheme()

    if check_usable(dir) is None:
        return

    dir, files = get_contents(dir, type)
    files = [file.split('/')[-1] for file in files]

    # Loop through files
        #   - Skip subDirectories
        #   - Check file extension matches type
        #   - Rename file, using either 'scheme'
        #   - if 'verbose', print original name and new name
        #   - if renamed, increase counter
        #   - if !renamed, increase other-counter
    for file in files:
        file_type = file.split('.')[-1]
        new_filename = f'{scheme}_{renamed_count:05d}.{file_type}'

        if verbose:
            print(f'{file} -> {new_filename}')

        old_des = dir + file
        new_des = dir + new_filename
        rename(old_des, new_des)

        renamed_count += 1
    else:
        dynamic_word = 'file' if renamed_count == 1 else 'files'
        report = f'{renamed_count} {dynamic_word} successfully renamed.'
        print(report)


def get_contents(dir, type):
    ammend = '' if dir[-1] == '/' else '/'
    dir = dir + ammend
    if type:
        pattern = dir + '*' + type
    else:
        pattern = dir + '*.*'

    files = glob.glob(pattern)
    return dir, files

def check_usable(dir):
    if not exists(dir):
        print('Not a valid path.')
        return None
    if not isdir(dir):
        print('Provided dir is not a directory.')
        return None
    if len(listdir(dir)) == 0:
        print('Directory is empty.')
        return None
    return dir

def get_scheme() -> str:
    date = datetime.date.today()
    format = '%Y.%m.%d'
    return date.strftime(format)

if __name__ == '__main__':
    arg_parser()