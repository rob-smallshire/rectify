from pprint import pprint as pp

from PIL import Image
from PIL.Image import QUAD, BICUBIC
from PIL.ImageDraw import Draw
from PIL.ImageOps import flip, grayscale, crop
from euclidian.cartesian2 import Line2, intersection2

from rectify.mountdetector import (find_mount_top_boundary,
                                   find_mount_bottom_boundary,
                                   find_mount_left_boundary,
                                   find_mount_right_boundary)


def draw_cross(context, position, radius, **kwargs):
    context.line((position.x - radius, position.y, position.x + radius, position.y), **kwargs)
    context.line((position.x, position.y - radius, position.x, position.y + radius), **kwargs)


# def draw():
#     boundary_image = flipped_image.copy()
#     draw = Draw(boundary_image)
#     draw.line((top_boundary_start.x, top_boundary_start.y, top_boundary_end.x, top_boundary_end.y), fill=(255, 255, 0), width=3)
#     draw.line((bottom_boundary_start.x, bottom_boundary_start.y, bottom_boundary_end.x, bottom_boundary_end.y), fill=(255, 255, 0), width=3)
#     draw.line((left_boundary_start.x, left_boundary_start.y, left_boundary_end.x, left_boundary_end.y), fill=(0, 255, 255), width=3)
#     draw.line((right_boundary_start.x, right_boundary_start.y, right_boundary_end.x, right_boundary_end.y), fill=(0, 255, 255), width=3)
#
#     draw_cross(draw, top_left_corner, radius=20, width=3, fill=(255, 0, 0))
#     draw_cross(draw, top_right_corner, radius=20, width=3, fill=(255, 0, 0))
#     draw_cross(draw, bottom_left_corner, radius=20, width=3, fill=(255, 0, 0))
#     draw_cross(draw, bottom_right_corner, radius=20, width=3, fill=(255, 0, 0))
#
#     boundary_image.save(output_filepath.replace('.jpg', '_boundary.jpg'))

def process_image_file(input_filepath, output_filepath, threshold):
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
    quad =  find_mount_boundary_quad(flipped_image, threshold)
    d = distortion(*quad)
    print("distortion =", d)
    extracted_image = extract_quad(flipped_image, *quad)
    cropped_image = crop_border(extracted_image, 16)
    cropped_image.save(output_filepath)


def find_mount_boundary_quad(flipped_image, threshold):
    gray_image = grayscale(flipped_image)
    top_boundary_start, top_boundary_end = find_mount_top_boundary(gray_image, threshold)
    bottom_boundary_start, bottom_boundary_end = find_mount_bottom_boundary(gray_image, threshold)
    left_boundary_start, left_boundary_end = find_mount_left_boundary(gray_image, threshold)
    right_boundary_start, right_boundary_end = find_mount_right_boundary(gray_image, threshold)
    top_boundary_line = Line2.through_points(top_boundary_start, top_boundary_end)
    bottom_boundary_line = Line2.through_points(bottom_boundary_start, bottom_boundary_end)
    left_boundary_line = Line2.through_points(left_boundary_start, left_boundary_end)
    right_boundary_line = Line2.through_points(right_boundary_start, right_boundary_end)
    top_left_corner = intersection2(top_boundary_line, left_boundary_line)
    top_right_corner = intersection2(top_boundary_line, right_boundary_line)
    bottom_left_corner = intersection2(bottom_boundary_line, left_boundary_line)
    bottom_right_corner = intersection2(bottom_boundary_line, right_boundary_line)
    print(top_left_corner)
    print(top_right_corner)
    print(bottom_left_corner)
    print(bottom_right_corner)
    return top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner


def distortion(top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner):
    dist_diagonal1 = top_left_corner.distance_to(bottom_right_corner)
    dist_diagonal2 = top_right_corner.distance_to(bottom_left_corner)
    dist_bottom, dist_left, dist_right, dist_top = quad_side_lengths(bottom_left_corner, bottom_right_corner,
                                                                     top_left_corner, top_right_corner)

    horizontal_distortion = (max(dist_top, dist_bottom) / min(dist_top, dist_bottom)) - 1
    vertical_distortion = (max(dist_left, dist_right) / min(dist_left, dist_right)) - 1
    diagonal_distortion = (max(dist_diagonal1, dist_diagonal2) / min(dist_diagonal1, dist_diagonal2)) - 1
    distortion = horizontal_distortion + vertical_distortion + diagonal_distortion
    print("{:.4f} + {:.4f} + {:.4f} = {:.4f}".format(horizontal_distortion, vertical_distortion, diagonal_distortion, distortion))
    return distortion


def quad_side_lengths(bottom_left_corner, bottom_right_corner, top_left_corner, top_right_corner):
    dist_top = top_left_corner.distance_to(top_right_corner)
    dist_bottom = bottom_left_corner.distance_to(bottom_right_corner)
    dist_left = top_left_corner.distance_to(bottom_left_corner)
    dist_right = top_right_corner.distance_to(bottom_right_corner)
    return dist_bottom, dist_left, dist_right, dist_top


def extract_quad(image, top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner):
    dist_bottom, dist_left, dist_right, dist_top = quad_side_lengths(bottom_left_corner, bottom_right_corner,
                                                                 top_left_corner, top_right_corner)
    extracted_width = round((dist_top + dist_bottom) / 2)
    extracted_height = round((dist_left + dist_right) / 2)
    extracted_image = image.transform(
        (extracted_width, extracted_height),
        QUAD,
        (top_left_corner.x, top_left_corner.y,
         bottom_left_corner.x, bottom_left_corner.y,
         bottom_right_corner.x, bottom_right_corner.y,
         top_right_corner.x, top_right_corner.y),
        BICUBIC)
    return extracted_image


def crop_border(image, border=16):
    cropped_image = crop(image, border=border)
    return cropped_image
