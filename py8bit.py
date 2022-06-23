import argparse
import logging
import os
import os.path
import sys

from PIL import Image


def pixelate(input_file_path, pixel_size, output_dir):
    image = Image.open(input_file_path)
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )

    file_parts = os.path.splitext(os.path.basename(input_file_path))
    basename = '%s-%dpx%s' % (file_parts[0], pixel_size, file_parts[1])
    outfile = os.path.join(output_dir, basename)
    image.save(outfile)
    logging.info('wrote to %s' % outfile)


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

    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    numeric_level = getattr(logging, args.logging_level.upper(), None)
    logging.basicConfig(level=numeric_level)

    for img in args.images:
        pixelate(img, args.pixel_size, args.output_dir)


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
