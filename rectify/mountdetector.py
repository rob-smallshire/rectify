import numpy
from euclidian.cartesian2 import Point2, Line2
from sklearn import linear_model

def find_mount_top_boundary(gray_image, threshold=40):
    # Find the top edge by walking down on each row until we pass the threshhold

    gray_pixels = gray_image.load()
    mount_boundary_points = []
    for x in range(gray_image.width):
        for y in range(gray_image.height):
            value = gray_pixels[x, y]
            if value >= threshold:
                mount_boundary_points.append((x, y))
                gray_pixels[x, y] = 255
                break
    mount_boundary_points_x = numpy.fromiter((p[0] for p in mount_boundary_points), float).reshape(-1, 1)
    mount_boundary_points_y = numpy.fromiter((p[1] for p in mount_boundary_points), float)

    model_ransac = linear_model.RANSACRegressor()
    model_ransac.fit(mount_boundary_points_x, mount_boundary_points_y)
    start = Point2(0, model_ransac.predict(0)[0])
    end = Point2(gray_image.width, model_ransac.predict(gray_image.width - 1)[0])
    return start, end


def find_mount_bottom_boundary(gray_image, threshold=40):
    # Find the top edge by walking down on each row until we pass the threshhold

    gray_pixels = gray_image.load()
    mount_boundary_points = []
    for x in range(gray_image.width):
        for y in reversed(range(gray_image.height)):
            value = gray_pixels[x, y]
            if value >= threshold:
                mount_boundary_points.append((x, y))
                gray_pixels[x, y] = 255
                break
    mount_boundary_points_x = numpy.fromiter((p[0] for p in mount_boundary_points), float).reshape(-1, 1)
    mount_boundary_points_y = numpy.fromiter((p[1] for p in mount_boundary_points), float)

    model_ransac = linear_model.RANSACRegressor()
    model_ransac.fit(mount_boundary_points_x, mount_boundary_points_y)
    start = Point2(0, model_ransac.predict(0)[0])
    end = Point2(gray_image.width, model_ransac.predict(gray_image.width - 1)[0])
    return start, end


def find_mount_left_boundary(gray_image, threshold=40):
    # Find the top edge by walking down on each row until we pass the threshhold

    gray_pixels = gray_image.load()
    mount_boundary_points = []
    for y in range(gray_image.height):
        for x in range(gray_image.width):
            value = gray_pixels[x, y]
            if value >= threshold:
                mount_boundary_points.append((x, y))
                gray_pixels[x, y] = 255
                break
    mount_boundary_points_x = numpy.fromiter((p[0] for p in mount_boundary_points), float)
    mount_boundary_points_y = numpy.fromiter((p[1] for p in mount_boundary_points), float).reshape(-1, 1)

    model_ransac = linear_model.RANSACRegressor()
    model_ransac.fit(mount_boundary_points_y, mount_boundary_points_x)
    start = Point2(model_ransac.predict(0)[0], 0)
    end = Point2(model_ransac.predict(gray_image.height - 1)[0], gray_image.height)
    return start, end


def find_mount_right_boundary(gray_image, threshold=40):
    # Find the top edge by walking down on each row until we pass the threshhold

    gray_pixels = gray_image.load()
    mount_boundary_points = []
    for y in range(gray_image.height):
        for x in reversed(range(gray_image.width)):
            value = gray_pixels[x, y]
            if value >= threshold:
                mount_boundary_points.append((x, y))
                gray_pixels[x, y] = 255
                break
    mount_boundary_points_x = numpy.fromiter((p[0] for p in mount_boundary_points), float)
    mount_boundary_points_y = numpy.fromiter((p[1] for p in mount_boundary_points), float).reshape(-1, 1)

    model_ransac = linear_model.RANSACRegressor()
    model_ransac.fit(mount_boundary_points_y, mount_boundary_points_x)
    start = Point2(model_ransac.predict(0)[0], 0)
    end = Point2(model_ransac.predict(gray_image.height - 1)[0], gray_image.height)
    return start, end