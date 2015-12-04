from PIL import Image
from PIL.ImageOps import flip, grayscale

from pprint import pprint as pp

from asq.initiators import query
from asq.selectors import a_

import rectify.asqext
from rectify.peakdetector import find_peak_base


def is_minima(a, b, c):
    """True if the series a, b, c has its minimum at b."""
    return b < a and b < c

def is_maxima(a, b, c):
    """True if the series a, b, c has its maximum at b."""
    return b > a and b > c


def find_indexed_element_for_first_minimum(histogram):
    return query(histogram)                              \
           .copy_padded_triples()                        \
           .select_with_index()                          \
           .where(lambda item: is_minima(*item.element)) \
           .select(a_('index'))                          \
           .first_or_default(0)


def find_indexed_element_for_first_maximum(histogram):
    return query(histogram)                               \
            .copy_padded_triples()                        \
            .select_with_index()                          \
            .where(lambda item: is_maxima(*item.element)) \
            .select(a_('index'))                          \
            .first_or_default(0)


def process_image_file(input_filepath, output_filepath):
    """Rotate and crop image.

    Args:
        input_filepath: Path to the source image.
        output_filepath: Path to the output image.

    Raises:
        OSError: file ops
    """
    if input_filepath == output_filepath:
        raise ValueError("Cannot overwrite input file.")
    input_image = Image.open(input_filepath)
    print(input_image.format, input_image.size, input_image.mode)
    flipped_image = flip(input_image)
    gray_image = grayscale(flipped_image)
    gray_image.save(output_filepath)
    histogram = gray_image.histogram()
    pp(len(histogram))

    # Find first minimum in grayscale histogram
    # Find base of dark spike to determine border threshhold
    first_minimum_index = find_indexed_element_for_first_minimum(histogram)
    print("first_minimum_index", first_minimum_index)
    first_maximum_index = find_indexed_element_for_first_maximum(histogram)
    print("first_maximum_index", first_maximum_index)
    pp(histogram)

    # Find first peak
    peak_base = find_peak_base(histogram, first_minimum_index, first_maximum_index)
    print(peak_base)

    thresholded_image = gray_image.point(lambda p: 0 if p <= peak_base else p)
    th = thresholded_image.histogram()
    pp(th)
    thresholded_image.save(output_filepath)