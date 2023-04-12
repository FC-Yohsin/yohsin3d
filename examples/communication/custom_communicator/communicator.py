from yohsin3d import BaseCommunicator


class CustomCommunicator(BaseCommunicator):
    def __init__(self) -> None:
        super().__init__()
        self.heard_data: str = None

    def say(self) -> None:
        self.said_message = f"HelloFromAgent{self.world_model.my_number}"

    def hear(self) -> str:
        heard_message = self.heard_message
        message = heard_message.message
        self.heard_data = message
