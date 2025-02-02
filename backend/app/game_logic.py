from app.schemas import ThrowTriplet


class AroundTheWorldGame:
    def __init__(self, mode: str, darts_per_target: int):
        self.mode = mode
        self.darts_per_target = darts_per_target
        self.current_target = 1
        self.completed_targets = []

    def process_triplet(self, triplet: ThrowTriplet) -> bool:
        # Logic for processing throws (similar to earlier implementation)
        pass

    def get_status(self):
        return {
            "current_target": self.current_target,
            "completed_targets": self.completed_targets,
        }
