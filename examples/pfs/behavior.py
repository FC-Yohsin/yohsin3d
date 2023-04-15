from yohsin3d import BaseBehavior
from yohsin3d.core.world import PlayModes
from yohsin3d.locomoters import PFSWalk, PFSTurn


class PFSBehavior(BaseBehavior):
    def __init__(self, start_coordinates=None, communicator=None, localizer=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=communicator, localizer=localizer)
        
    def initialize_behavior(self):
        self.pfs_walk = PFSWalk(self.body_model, self.world_model, self.localizer)
        self.pfs_turn = PFSTurn(self.body_model, self.world_model, self.localizer)

    def act(self):
        if self.world_model.playmode == PlayModes.PLAY_ON:

            # Walk and stop at target
            self.pfs_walk.walk_to(
                target=(0, 0),
            )

            ## Dribble ball to goal
            # self.pfs_walk.dribble_to_goal()

            ## Turn to target orientation
            # self.pfs_turn.execute_turn_orientation(theta=-180)
