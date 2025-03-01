from games.utils.schemas import ThrowTriplet, Throw


class CountdownGame:
    """Class to manage a game of Countdown darts."""

    DOUBLE_VALUES = {2 * i for i in range(1, 21)} | {50}  # All doubles + bullseye
    SCORES = {
        "S": range(1, 21),
        "D": DOUBLE_VALUES,
        "T": {3 * i for i in range(1, 21)},
        "B": {25, 50},
    }

    def __init__(self, start_score: int = 501, double_in: bool = False, double_out: bool = False):
        self.start_score = start_score
        self.double_in = double_in
        self.double_out = double_out
        self.current_score = start_score
        self.in_play = not double_in
        self.throws: list[tuple[str, int]] = []  # List of (multiplier, value)

    def process_triplet(self, triplet: ThrowTriplet):
        return

    def throw(self, multiplier: str, value: int) -> bool:
        """Registers a throw if it's valid, updating the score accordingly."""
        if multiplier not in self.SCORES or value not in self.SCORES[multiplier]:
            return False  # Invalid throw

        score = {"S": 1, "D": 2, "T": 3, "B": 1}[multiplier] * value

        if self.double_in and not self.in_play:
            if multiplier == "D":
                self.in_play = True
            else:
                return False  # Must double in first

        new_score = self.current_score - score

        if new_score < 0 or (self.double_out and new_score == 0 and multiplier != "D"):
            return False  # Bust or invalid checkout

        self.current_score = new_score
        self.throws.append((multiplier, value))
        return True

    def is_finished(self) -> bool:
        """Returns True if the game is finished."""
        return self.current_score == 0

    def checkout_options(self) -> list[list[tuple[str, int]]]:
        """Returns possible checkout combinations if within 3 darts."""
        return self._find_checkouts(self.current_score, 3, self.double_out)

    @staticmethod
    def _find_checkouts(
        score: int, darts: int, require_double: bool
    ) -> list[list[tuple[str, int]]]:
        """Recursive function to find valid checkout combinations."""
        if score == 0:
            return [[]]
        if darts == 0 or score < 2:
            return []

        checkouts = []

        for multiplier, values in CountdownGame.SCORES.items():
            for value in values:
                points = {"S": 1, "D": 2, "T": 3, "B": 1}[multiplier] * value
                if points > score:
                    continue
                if darts == 1 and require_double and multiplier != "D":
                    continue

                remaining = CountdownGame._find_checkouts(
                    score - points, darts - 1, require_double and score - points > 0
                )
                for seq in remaining:
                    checkouts.extend([(multiplier, value)] * seq)

        return checkouts
