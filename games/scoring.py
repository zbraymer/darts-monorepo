from .utils import constants as c


def map_angle_to_segment(angle):
    # Define the dartboard segments in their correct order
    segments = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
    segment_angle = 360 / 20  # Each segment spans 18 degrees

    # Adjust angle by 9 degrees to align 0 degrees with the midpoint of segment 6
    adjusted_angle = (angle + 9) % 360

    # Determine the segment index
    segment_index = int(adjusted_angle // segment_angle) % 20
    return segments[segment_index]


def calculate_score(radius: float, angle: float):
    angle = (angle + 360) % 360  # Adjust angle to [0, 360)

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
    return {
        "multiplier": c.INGLE,
        "zone": map_angle_to_segment(angle),
        "score": map_angle_to_segment(angle) * c.SINGLE,
    }
