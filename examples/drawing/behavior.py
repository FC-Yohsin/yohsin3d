from yohsin3d import BaseBehavior
from drawing import rvDraw, Color
from yohsin3d.localizers import GroundTruthLocalizer


class DrawingBehavior(BaseBehavior):
    def __init__(self, start_coordinates=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=None, localizer=GroundTruthLocalizer())

    def act(self):
        if self.localizer.my_location.position:
            rvDraw.draw_circle(self.localizer.my_location.position, radius=0.15, color=Color.BLUE, name="my_location")
        if self.localizer.ball_position:
            rvDraw.draw_circle(self.localizer.ball_position, radius=0.1, color=Color.RED, name="ball_position")
     
