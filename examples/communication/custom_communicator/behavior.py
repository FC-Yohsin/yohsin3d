from yohsin3d import BaseBehavior
from communicator import CustomCommunicator

class CustomCommunicatorBehavior(BaseBehavior):
    def __init__(self, start_coordinates = None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=CustomCommunicator())
        self.communicator: CustomCommunicator

    def act(self):
        if self.communicator.heard_data:
            print(f"Agent {self.world_model.my_number} recieved following message: {self.communicator.heard_data}")
