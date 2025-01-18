from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the input data structure
class PolarCoordinates(BaseModel):
    radius: float  # Normalized radius (0.0 to 1.0)
    angle: float  # Angle in degrees (-180 to 180)


@app.get("/calculate-score")
async def calculate_score(radius: float, angle: float):
    radius = radius
    angle = (angle + 360) % 360  # Adjust angle to [0, 360)

    # Define scoring zones
    if radius <= 0.025:
        return {"zone": "Inner Bullseye", "score": 50}
    if radius <= 0.065:
        return {"zone": "Outer Bullseye", "score": 25}
    if 0.40 <= radius <= 0.43:
        return {"zone": "Triple Ring", "score": map_angle_to_segment(angle) * 3}
    if 0.65 <= radius <= 0.68:
        return {"zone": "Double Ring", "score": map_angle_to_segment(angle) * 2}
    if radius > 1.0:
        return {"zone": "Miss", "score": 0}

    # Otherwise, it's a single score
    return {"zone": "Single", "score": map_angle_to_segment(angle)}


def map_angle_to_segment(angle):
    # Define the dartboard segments in their correct order
    segments = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
    segment_angle = 360 / 20  # Each segment spans 18 degrees

    # Adjust angle by 9 degrees to align 0 degrees with the midpoint of segment 6
    adjusted_angle = (angle + 9) % 360

    # Determine the segment index
    segment_index = int(adjusted_angle // segment_angle) % 20
    return segments[segment_index]
