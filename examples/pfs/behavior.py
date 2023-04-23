from yohsin3d import BaseBehavior
from yohsin3d.core.world import PlayModes
from yohsin3d.locomotors import PFSWalk, PFSTurn, FallRecovery


class PFSBehavior(BaseBehavior):
    def __init__(self, start_coordinates=None, communicator=None, localizer=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=communicator, localizer=localizer)
        
    def initialize_behavior(self):
        self.pfs_walk = PFSWalk(self.body_model, self.world_model, self.localizer)
        self.pfs_turn = PFSTurn(self.body_model, self.world_model, self.localizer)
        self.fall_recovery = FallRecovery(self.body_model, self.world_model)

    def act(self):

        if not self.fall_recovery.detect_fall_and_getup():
            if self.world_model.playmode == PlayModes.PLAY_ON:            
                self.pfs_walk.dribble_walk()
        else:
            self.pfs_walk.reset()