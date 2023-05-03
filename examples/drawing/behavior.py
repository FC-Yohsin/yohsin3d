from yohsin3d import BaseBehavior
from drawing import rvDraw, Color
from yohsin3d.localizers import GroundTruthLocalizer, GeometricLocalizer


class DrawingBehavior(BaseBehavior):
    def __init__(self, start_coordinates=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=None, localizer=GeometricLocalizer())

    def act(self):
        if self.localizer.my_location.position:
            print(self.localizer.my_location)
            rvDraw.draw_circle(self.localizer.my_location.position,
                               radius=0.015, color=Color.BLUE, name="my_location")
        if self.localizer.ball_position:
            rvDraw.draw_circle(self.localizer.ball_position,
                               radius=0.01, color=Color.BLUE, name="ball_position")
