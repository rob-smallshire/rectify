from asq.initiators import query
from euclidian.cartesian2 import Point2, Line2


def find_peak_base(sequence, maxima_index, minima_index):
    """Find the index of the base of the peak.

    Args:
        sequence: A sequence of data in which to locate the peak base.
        maxima_index: The index of an item in sequence on or near the top of the peak.
        minima_index: The index of an item in sequence off or away from the peak.

    Returns:
        The index of the estimated base of the peak.
    """
    p = Point2(maxima_index, sequence[maxima_index])
    q = Point2(minima_index, sequence[minima_index])
    basis_line = Line2.through_points(p, q)

    query_points = query(Point2(index, sequence[index]) for index in range(minima_index, maxima_index))
    base_point = query_points                    \
                 .select(basis_line.distance_to) \
                 .max_index(start=minima_index)
    return base_point.index








