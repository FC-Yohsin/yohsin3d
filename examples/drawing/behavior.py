from yohsin3d import BaseBehavior
from yohsin3d.locomotors import PFSWalk
from drawing import rvDraw, Color
from yohsin3d.localizers import GeometricLocalizer


class DrawingBehavior(BaseBehavior):
    def __init__(self, start_coordinates=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=None, localizer=GeometricLocalizer())


    def initialize_behavior(self):
        self.pfs_walk = PFSWalk(self.body_model, self.world_model, self.localizer)
        

    def act(self):
        if self.localizer.my_location.position:
            rvDraw.draw_circle(self.localizer.my_location.position, radius=0.15, color=Color.BLUE.value, name="my_location")

        self.pfs_walk.walk_to((0,0))
