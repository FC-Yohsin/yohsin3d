class AgentLocation:
    def __init__(self) -> None:
        self.position = None
        self.orientation = None

        self.previos_position = None
        self.previos_orientation = None

    def update_position(self, position):
        self.previos_position = self.position
        self.position = position

    def update_orientation(self, orientation):
        self.previos_orientation = self.orientation
        self.orientation = orientation
