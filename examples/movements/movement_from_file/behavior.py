from yohsin3d import BaseBehavior
from yohsin3d.movement import Movement
from skills import wave_skill


class MovementBehavior(BaseBehavior):
    def __init__(self, start_coordinates: None, communicator=None, localizer=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=communicator,  localizer=localizer)

    def act(self):
        wave_skill.perform(self.body_model, self.world_model)
        if wave_skill.is_finished():
            wave_skill.reset()
