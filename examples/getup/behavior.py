from yohsin3d import BaseBehavior
from yohsin3d.movement import Movement
from yohsin3d.locomotors import FallRecovery


FALL_ON_BACK_SKILL = '''
start phase 0: 2.0 
target lle5 -60 7.0 
target rle5 -60 7.0 
end phase
'''

FALL_ON_FRONT_SKILL = ''' 
start phase 0: 2.0 
target lle5 60 7.0 
target rle5 60 7.0 
end phase
'''

class GetUpBehavior(BaseBehavior):
    def __init__(self, start_coordinates=None, communicator=None, localizer=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=communicator, localizer=localizer)
        
        self.back_falling = False
        self.fall_on_back_skill: Movement = Movement.from_string(FALL_ON_BACK_SKILL)
        self.fall_on_front_skill: Movement = Movement.from_string(FALL_ON_FRONT_SKILL)
        
    def initialize_behavior(self):
        self.fall_recoverer = FallRecovery(self.body_model, self.world_model)

    def act(self):
        if not self.fall_recoverer.detect_fall_and_getup():
            if self.back_falling:
                self.fall_on_back_skill.perform(self.body_model, self.world_model)
                if self.fall_on_back_skill.is_finished():
                    self.back_falling = False
            else:
                self.fall_on_front_skill.perform(self.body_model, self.world_model)
                if self.fall_on_front_skill.is_finished():
                    self.back_falling = True    
        else:
            if self.back_falling: self.fall_on_front_skill.reset()
            else:  self.fall_on_back_skill.reset()
        
                