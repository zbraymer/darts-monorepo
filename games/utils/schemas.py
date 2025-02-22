from dataclasses import dataclass


@dataclass
class Throw:
    radius: float
    angle: float


@dataclass
class ThrowTriplet:
    target: str
    throws: list[Throw]


@dataclass
class GameCreate:
    mode: str
    darts_per_target: int


@dataclass
class GameStatus:
    current_target: int
    completed_targets: list[int]
    throws: list[ThrowTriplet]
    mode: str
    darts_per_target: int
