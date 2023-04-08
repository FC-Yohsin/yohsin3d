from ..common import AgentLocation
from ..world import WorldModel


class BaseLocalizer:
    def _init_(self) -> None:
        self.world_model: WorldModel = None
        self.my_location = AgentLocation()
        self.ball_position = None

    def initialize(self, world_model: WorldModel) -> None:
        self.world_model = world_model

    def update(self) -> None:
        pass
