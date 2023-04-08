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


GROUNDTRUTH_NOT_ENABLED_ERROR = "Ground truth not enabled"
class GroundTruthLocalizer(BaseLocalizer):
    def _init_(self) -> None:
        super()._init_()

    def check_validity(self) -> None:
        assert self.world_model.groundtruth.is_enabled(), GROUNDTRUTH_NOT_ENABLED_ERROR

    def update(self) -> None:
        self.check_validity()
        self.my_location = self.world_model.groundtruth.my_location
        self.ball_position = self.world_model.groundtruth.ball_position
    