class AgentLocation:
    def __init__(self, position=None, orientation=None) -> None:
        self.position = position
        self.orientation = orientation

    def update_position(self, position):
        self.position = position

    def update_orientation(self, orientation):
        self.orientation = orientation

    def __repr__(self) -> str:
        return f"AgentLocation(position={self.position}, orientation={self.orientation})"
