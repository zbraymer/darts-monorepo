import app.constants as c
from app.schemas import Throw, ThrowScore

import random
import math
from app import constants as c
from app.schemas import Throw


def generate_throw_for_score(zone: int, multiplier: str) -> Throw:
    """
    Generates a random Throw (radius and angle) that corresponds to the given zone and multiplier.

    Parameters
    ----------
    zone : int
        The dartboard zone number (1-20) or special zones like 25 for outer bullseye and 50 for inner bullseye.
    multiplier : str
        The score multiplier: 'single', 'double', 'triple', or 'bull' for bullseyes.

    Returns
    -------
    Throw
        A Throw object with random radius and angle corresponding to the specified zone and multiplier.
    """
    if multiplier not in {c.SINGLE, c.DOUBLE, c.TRIPLE, "bull"}:
        raise ValueError("Invalid multiplier. Must be 'single', 'double', 'triple', or 'bull'.")

    if multiplier == "bull":
        if zone == c.INNER:
            # Inner Bullseye
            radius = random.uniform(0, c.INNER_BULL_RADIUS)
        elif zone == c.OUTER:
            # Outer Bullseye
            radius = random.uniform(c.INNER_BULL_RADIUS, c.OUTER_BULL_RADIUS)
        else:
            raise ValueError("Invalid zone for bullseye. Must be 25 (outer) or 50 (inner).")
        angle = random.uniform(0, 360)
    else:
        if zone < 1 or zone > 20:
            raise ValueError("Invalid zone. Must be between 1 and 20 for non-bullseye throws.")

        # Determine angle range for the specified zone
        segments = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
        segment_index = segments.index(zone)
        segment_angle = 360 / 20  # Each segment spans 18 degrees
        segment_center_angle = segment_index * segment_angle

        # Random angle within the segment
        angle = random.uniform(segment_center_angle - 9, segment_center_angle + 9) % 360

        # Determine radius range based on multiplier
        if multiplier == c.SINGLE:
            if random.choice([True, False]):
                radius = random.uniform(c.OUTER_BULL_RADIUS, c.INNER_TRIPLE_RADIUS)
            else:
                radius = random.uniform(c.OUTER_TRIPLE_RADIUS, c.INNER_DOUBLE_RADIUS)
        elif multiplier == c.DOUBLE:
            radius = random.uniform(c.INNER_DOUBLE_RADIUS, c.OUTER_DOUBLE_RADIUS)
        elif multiplier == c.TRIPLE:
            radius = random.uniform(c.INNER_TRIPLE_RADIUS, c.OUTER_TRIPLE_RADIUS)

    return Throw(radius=radius, angle=angle)


def map_angle_to_segment(angle):
    """_summary_

    Parameters
    ----------
    angle : float
        Angle in radians of throw of single dart.

    Returns
    -------
    int
        Zone that angle maps to.
    """
    # Define the dartboard segments in their correct order
    segments = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
    segment_angle = 360 / 20  # Each segment spans 18 degrees

    # Adjust angle by 9 degrees to align 0 degrees with the midpoint of segment 6
    adjusted_angle = (angle + 9) % 360

    # Determine the segment index
    segment_index = int(adjusted_angle // segment_angle) % 20
    return segments[segment_index]


def calculate_score(throw: Throw):
    """function to calculate score of a single dart

    Parameters
    ----------
    throw : Throw
        Radius and angle of a given dart throw.

    Returns
    -------
    dict
        dictionary of the multiplier, zone, and score
    """
    angle = (throw.angle + 360) % 360  # Adjust angle to [0, 360)
    radius = throw.radius

    # Define scoring zones
    if radius <= c.INNER_BULL_RADIUS:
        return {"multiplier": c.SINGLE, "zone": "Inner Bullseye", "score": c.SINGLE * c.INNER}
    if radius <= c.OUTER_BULL_RADIUS:
        return {"multiplier": c.SINGLE, "zone": "Outer Bullseye", "score": c.SINGLE * c.OUTER}
    if c.INNER_TRIPLE_RADIUS <= radius <= c.OUTER_TRIPLE_RADIUS:
        return {
            "multiplier": c.TRIPLE,
            "zone": map_angle_to_segment(angle),
            "score": map_angle_to_segment(angle) * c.TRIPLE,
        }
    if c.INNER_BULL_RADIUS <= radius <= c.OUTER_DOUBLE_RADIUS:
        return {
            "multiplier": c.TRIPLE,
            "zone": map_angle_to_segment(angle),
            "score": map_angle_to_segment(angle) * c.TRIPLE,
        }
    if radius > c.OUTER_DOUBLE_RADIUS:
        return {"zone": "Miss", "score": 0}

    # Otherwise, it's a single score
    return ThrowScore(
        multiplier=c.SINGLE,
        zone=map_angle_to_segment(angle),
        score=map_angle_to_segment(angle) * c.SINGLE,
    )
