from .world.world_model import WorldModel
from typing import Tuple



class BaseLocalizer:

    def _init_(self) -> None:
        self.world_model: WorldModel = None

    def initialize(self, world_model: WorldModel) -> None:
        self.world_model = world_model
    
    def localize_agent_position(self) -> Tuple[float, float, float]:
        pass

    def localize_agent_orientation(self) -> float:
        pass

    def localize_ball(self) -> Tuple[float, float, float]:
        pass


GROUNDTRUTH_NOT_ENABLED_ERROR = "Ground truth not enabled"
class GroundTruthLocalizer(BaseLocalizer):
    def _init_(self) -> None:
        super()._init_()

    def check_validity(self) -> None:
        assert self.world_model.groundtruth.is_enabled(), GROUNDTRUTH_NOT_ENABLED_ERROR

    def localize_agent_position(self) -> Tuple[float, float, float]:
        self.check_validity()
        return self.world_model.groundtruth.location.position
    
    def localize_agent_orientation(self) -> float:
        self.check_validity()
        return self.world_model.groundtruth.location.orientation
    
    def localize_ball(self) -> Tuple[float, float, float]:
        self.check_validity()
        return self.world_model.groundtruth.ball_position