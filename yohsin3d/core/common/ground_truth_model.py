from .agent_location import AgentLocation


class GroundTruthModel:
    def __init__(self):
        self.my_location = AgentLocation()
        self.ball_position = None

    def is_enabled(self):
        return self.my_location.position is not None and self.my_location.orientation is not None and self.ball_position is not None
