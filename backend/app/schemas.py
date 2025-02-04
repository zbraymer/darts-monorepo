from pydantic import BaseModel


class Throw(BaseModel):
    radius: float
    angle: float


class ThrowTriplet(BaseModel):
    target: str
    throws: list[Throw]


class ThrowScore(BaseModel):
    multiplier: int
    zone: int
    score: int


class GameCreate(BaseModel):
    mode: str
    darts_per_target: int


class GameStatus(BaseModel):
    current_target: int
    completed_targets: list[int]
    throws: list[ThrowTriplet]
    mode: str
    darts_per_target: int
