
from ..core import BaseLocalizer


GROUNDTRUTH_NOT_ENABLED_ERROR = "Ground truth not enabled"


class Y3dLocalizer(BaseLocalizer):
    def __init__(self) -> None:
        super().__init__()

    def check_validity(self) -> None:
        assert self.world_model.groundtruth.is_enabled(), GROUNDTRUTH_NOT_ENABLED_ERROR

    def update(self) -> None:
        self.check_validity()
        self.my_location = self.world_model.groundtruth.my_location
        self.ball_position = self.world_model.groundtruth.ball_position
