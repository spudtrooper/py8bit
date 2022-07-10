import argparse
import logging
import os
import os.path
import sys

from PIL import Image


def pixelate(input_file_path, outfile, pixel_size):
    image = Image.open(input_file_path)
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )

    image.save(outfile)

def main(prog, args):
    parser = argparse.ArgumentParser(description='Pixelate images')
    parser.add_argument('--images', nargs='+', type=str,
                        required=True, help='list of images to convert')
    parser.add_argument('-p', '--pixel_size', type=int, required=False, default=10,
                        help='the size of each new pixel, in pixels of the original image')
    parser.add_argument('-d', '--output_dir', type=str,
                        required=True, help='output directory')
    parser.add_argument('-l', '--logging_level', type=str, default='DEBUG',
                        required=False, help='logging level')
    parser.add_argument('-s', '--skip_existing_file', type=bool, default=False,
                        required=False, help='Skip existing file')
    parser.add_argument('-c', '--continue_after_errors', type=bool, default=False,
                        required=False, help='Continue after errors')

    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    numeric_level = getattr(logging, args.logging_level.upper(), None)
    logging.basicConfig(level=numeric_level)

    for img in args.images:
        file_parts = os.path.splitext(os.path.basename(img))
        basename = '%s-%dpx%s' % (file_parts[0], args.pixel_size, file_parts[1])
        outfile = os.path.join(args.output_dir, basename)
        if args.skip_existing_file and os.path.exists(outfile):
          logging.info('skip existing %s', outfile)
          continue
        try:
          pixelate(img, outfile, args.pixel_size)
        except OSError as e:
          if args.continue_after_errors:
            logging.info('error: %s', e)
          else:
              raise e
        logging.info('wrote to %s' % outfile)


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
