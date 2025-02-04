from app import constants as c
from app.schemas import ThrowTriplet
from app.utils import calculate_score


class AroundTheWorldGame:
    """
    Represents the "Around the World" dart game.

    Attributes
    ----------
    mode : str
        The game mode, which determines the required hit type ("single", "double", "triple").
    darts_per_turn : int
        The number of darts thrown per turn.
    current_target : int
        The current number the player needs to hit (starts at 1 and ends at 20).
    is_complete : bool
        Indicates whether the game has been completed.
    """

    def __init__(self, mode: str = "single") -> None:
        """
        Initializes an AroundTheWorldGame instance.

        Parameters
        ----------
        mode : str, optional
            The game mode, either "single", "double", or "triple" (default is "single").

        """
        if mode not in {"single", "double", "triple"}:
            raise ValueError("Invalid mode. Must be 'single', 'double', or 'triple'.")

        self.mode = mode
        self.current_target = 1  # Start at 1
        self.throw_count = 0
        self.is_complete = False

    def process_throws(self, throws: ThrowTriplet) -> dict:
        """
        Processes a set of dart throws for a turn.

        Parameters
        ----------
        throws : ThrowTriplet
            A class representing a set of 3 dart throws.

        Returns
        -------
        dict
            The updated game state.
        """
        if self.is_complete:
            return {"message": "Game is already completed.", "current_target": self.current_target}

        # Check if the required target was hit in any throw
        for throw in throws.throws:
            score = calculate_score(throw)
            self.throw_count += 1

            if (score.multiplier == self.mode) and (score.zone == self.current_target):
                self.current_target += 1

            if self.current_target > c.TWENTY:
                self.is_complete = True
                return {"message": "Game Complete"}

            # TODO Need to understand how to process sequential hits from a throw target perspective

        return {"message": "Turn processed.", "current_target": self.current_target}

    def get_game_state(self) -> dict:
        """
        Returns the current state of the game.

        Returns
        -------
        dict
            The game state including the current target and completion status.
        """
        return {
            "current_target": self.current_target,
            "is_complete": self.is_complete,
        }
