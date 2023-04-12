from yohsin3d import BaseBehavior


class SoccerBehavior(BaseBehavior):
    def __init__(self, start_coordinates=None, communicator=None, localizer=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=communicator,  localizer=localizer)

    def act(self):
        pass
