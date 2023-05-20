#! /usr/bin/env python3
# Benjamin White

import argparse
import logging
import os

# pip extras
import pillow_heif

from PIL import Image


def get_files(path, ext):
    log = logging.getLogger(__name__)

    try:
        items_at_path = os.listdir(path)
        return [os.path.join(path, item) for item in items_at_path if not os.path.isdir(os.path.join(path, item)) and item.endswith(ext)]
    except (PermissionError, NotADirectoryError) as e:
        log.error(e)


def convert_files(args, files_to_convert):
    log = logging.getLogger(__name__)
    try:
        os.makedirs(args.output_path)
    except (PermissionError, FileExistsError) as e:
        log.debug(e)

    for f in files_to_convert:
        heif_file = pillow_heif.read_heif(f)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw"
        )

        src_path, file_name = os.path.split(f)
        old_file_name, _ = os.path.splitext(file_name)
        new_file_name = f'{old_file_name}.{args.file_format}'
        output_file_name = os.path.join(args.output_path, new_file_name)

        image.save(output_file_name, format=args.file_format)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', default=0, action='count', help='Be more verbose.')
    parser.add_argument('-p', '--path', required=True, help='Parent directory of files to convert')
    parser.add_argument('-t', '--type', required=False, default='HEIC', help='File extension to look for.')
    parser.add_argument('-o', '--output_path', required=True, help='Directory to place converted files.')
    parser.add_argument('-f', '--file_format', required=True, help='Output file format.')

    args = parser.parse_args()

    log_format = '[%(asctime)s] [%(name)s] <%(levelname)s> %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG if args.verbose >= 1 else logging.INFO)
    log = logging.getLogger(__name__)

    files_to_convert = get_files(args.path, args.type)

    log.info(f'{len(files_to_convert)} files to convert')

    if args.verbose:
        for f in files_to_convert:
            log.debug('Files to convert:')
            log.debug(f)

    convert_files(args, files_to_convert)


if __name__ == '__main__':
    main()

