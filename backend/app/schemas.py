from pydantic import BaseModel


class ThrowScore(BaseModel):
    """
    Represents the score of a single dart throw.

    Attributes
    ----------
    multiplier : int
        The multiplier applied to the base score (e.g., 1 for single, 2 for double, 3 for triple).
    zone : int
        The dartboard zone number hit by the throw.
    score : int
        The total score calculated as `multiplier` * `zone`.
    """

    multiplier: int
    zone: int
    score: int


class Throw(BaseModel):
    """
    Represents a single dart throw with its polar coordinates.

    Attributes
    ----------
    radius : float
        The radial distance from the center of the dartboard to the point of impact.
    angle : float
        The angle (in degrees) from a reference direction to the point of impact.
    """

    radius: float
    angle: float


class ThrowTriplet(BaseModel):
    """
    Represents a set of three dart throws aimed at a specific target.

    Attributes
    ----------
    target : str
        The intended target for the set of throws.
    throws : list of Throw
        A list containing three Throw instances representing the individual dart throws.
    """

    target: str
    throws: list[Throw]


class GameCreate(BaseModel):
    """
    Represents the initial configuration for creating a new dart game.

    Attributes
    ----------
    mode : str
        The game mode, determining the required hit type (e.g., 'single', 'double', 'triple').
    darts_per_target : int
        The number of darts thrown per target in the game.
    """

    mode: str
    darts_per_target: int


class GameStatus(BaseModel):
    """
    Represents the current status of an ongoing dart game.

    Attributes
    ----------
    current_target : int
        The current number the player needs to hit.
    completed_targets : list of int
        A list of target numbers that have been successfully hit.
    throws : list of ThrowTriplet
        A list of ThrowTriplet instances representing the sets of throws made.
    mode : str
        The game mode, determining the required hit type.
    darts_per_target : int
        The number of darts thrown per target in the game.
    """

    current_target: int
    completed_targets: list[int]
    throws: list[ThrowTriplet]
    mode: str
    darts_per_target: int
