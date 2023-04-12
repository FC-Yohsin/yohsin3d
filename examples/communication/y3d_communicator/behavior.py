from yohsin3d import BaseBehavior
from yohsin3d.communicators import Y3dCommunicator
from yohsin3d.localizers import GroundTruthLocalizer

class Y3dCommunicatorBehavior(BaseBehavior):
    def __init__(self, start_coordinates = None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=Y3dCommunicator(), localizer=GroundTruthLocalizer())
        self.communicator: Y3dCommunicator

    def act(self):
        if self.communicator.heard_data:
            print(f"Agent {self.world_model.my_number} recieved following communication data: {self.communicator.heard_data}")
