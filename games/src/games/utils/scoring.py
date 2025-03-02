from games.utils import constants as c


def map_angle_to_segment(angle: float) -> int:
    """
    Maps an angle to the corresponding dartboard segment.

    Parameters
    ----------
    angle : float
        The angle in degrees, measured from the 0-degree reference.

    Returns
    -------
    int
        The dartboard segment number (1-20) corresponding to the given angle.
    """
    segments = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
    segment_angle = 360 / 20  # Each segment spans 18 degrees
    adjusted_angle = (angle + 9) % 360  # Aligns 0 degrees with segment 6
    segment_index = int(adjusted_angle // segment_angle) % 20
    return segments[segment_index]


def get_multipleier(radius: float) -> int:
    """
    Determines the multiplier for a given radial distance on the dartboard.

    Parameters
    ----------
    radius : float
        The radial distance from the center of the dartboard.

    Returns
    -------
    int
        The multiplier applied to the throw (1 for single, 2 for double, 3 for triple).
    """
    if radius <= c.INNER_BULL_RADIUS:
        return c.SINGLE
    if c.INNER_BULL_RADIUS < radius <= c.OUTER_BULL_RADIUS:
        return c.SINGLE
    if c.INNER_TRIPLE_RADIUS < radius <= c.OUTER_TRIPLE_RADIUS:
        return c.TRIPLE
    if c.INNER_DOUBLE_RADIUS < radius <= c.OUTER_DOUBLE_RADIUS:
        return c.DOUBLE
    if radius > c.OUTER_DOUBLE_RADIUS:
        return 0
    return c.SINGLE
