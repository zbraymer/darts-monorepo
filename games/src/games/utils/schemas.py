from dataclasses import dataclass
from collections.abc import Iterator

from games.utils.scoring import map_angle_to_segment, get_multipleier


@dataclass
class Throw:
    """
    Represents a single dart throw with a radius and angle.

    Attributes
    ----------
    radius : float
        The radial distance from the center of the dartboard.
    angle : float
        The angle of the throw in degrees.
    """

    radius: float
    angle: float

    def get_score(self) -> "ThrowScore":
        """
        Computes the score of the throw based on the dartboard zones.

        Returns
        -------
        ThrowScore
            The calculated score including zone and multiplier.
        """
        zone = map_angle_to_segment(self.angle)
        multiplier = get_multipleier(self.radius)

        return ThrowScore(multiplier=multiplier, zone=zone, score=zone * multiplier)


@dataclass
class ThrowTriplet:
    """
    Represents a set of three dart throws.

    Attributes
    ----------
    throws : list[Throw]
        A list of three Throw instances representing a full turn.
    """

    throws: list[Throw]

    def __iter__(self) -> Iterator[Throw]:
        """
        Returns an iterator over the three dart throws.

        Returns
        -------
        Iterator[Throw]
            An iterator over the throws in this triplet.
        """
        return iter(self.throws)


@dataclass
class ThrowScore:
    """
    Represents the computed score of a single dart throw.

    Attributes
    ----------
    multiplier : int
        The multiplier applied to the throw (1 for single, 2 for double, 3 for triple).
    zone : int
        The dartboard segment hit (values from 1 to 20).
    score : int
        The final score for the throw (zone * multiplier).
    """

    multiplier: int
    zone: int
    score: int
