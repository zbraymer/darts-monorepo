from games.utils import constants as c


class AroundTheWorld:
    """
    Class to handle playing around the world.
    """

    def __init__(self, mode: str, darts_per_target: int):
        """
        Initialize the game.

        Parameters
        ----------
        mode : str
            The scoring mode ("singles", "doubles", "triples").
        darts_per_target : int
            The number of darts required to complete each target (1, 2, or 3).
        """
        if mode not in {"singles", "doubles", "triples"}:
            raise ValueError("Mode must be one of 'singles', 'doubles', or 'triples'.")
        if darts_per_target not in {1, 2, 3}:
            raise ValueError("Darts per target must be 1, 2, or 3.")

        self.mode = mode
        self.darts_per_target = darts_per_target
        self.current_target = 1
        self.completed_targets: dict[int, int] = {}  # Track throws required for each target
        self.total_throws = 0  # Total throws made
        self.current_target_hits = 0  # Successful hits on the current target

    def throw_dart(self, target: int, multiplier: int) -> bool:
        """
        Process a dart throw.

        Parameters
        ----------
        target : int
            The target number the player aimed for.
        multiplier : int
            The multiplier achieved (1 for single, 2 for double, 3 for triple).

        Returns
        -------
        bool
            True if the throw was successful, False otherwise.
        """
        self.total_throws += 1  # Increment total throws

        # Check if the throw hits the current target with the correct multiplier
        required_multiplier = {"singles": 1, "doubles": 2, "triples": 3}[self.mode]
        if target == self.current_target and multiplier == required_multiplier:
            self.current_target_hits += 1
        else:
            return False

        # Check if the target is complete
        if self.current_target_hits >= self.darts_per_target:
            self.completed_targets[self.current_target] = self.total_throws
            self.current_target += 1
            self.current_target_hits = 0  # Reset hits for the next target

        return True

    def is_game_over(self) -> bool:
        """
        Check if the game is over.

        Returns
        -------
        bool
            True if all targets are completed, False otherwise.
        """
        return self.current_target > c.TWENTY

    def get_game_status(self) -> dict:
        """
        Get the current game status.

        Returns
        -------
        dict
            The current game state.
        """
        return {
            "current_target": self.current_target,
            "completed_targets": self.completed_targets,
            "total_throws": self.total_throws,
            "mode": self.mode,
            "darts_per_target": self.darts_per_target,
        }
