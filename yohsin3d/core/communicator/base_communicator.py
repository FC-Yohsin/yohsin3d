from ..world import WorldModel
from ..localizer import BaseLocalizer
from ..common import NUM_AGENTS


class HeardMessage:
    def __init__(self) -> None:
        self.message = None
        self.heard_time = None
        self.team_name = None
        self.voice_orientation = None

    def update(self, message, heard_time, team_name, voice_orientation):
        self.message = message
        self.heard_time = heard_time
        self.team_name = team_name
        self.voice_orientation = voice_orientation


class BaseCommunicator:

    def __init__(self) -> None:
        self.said_message: str = ""
        self.heard_message: HeardMessage = HeardMessage()
        self.world_model: WorldModel = None
        self.localizer: BaseLocalizer = None

    def initialize(self, world_model: WorldModel,
                   localizer: BaseLocalizer) -> None:
        self.world_model = world_model
        self.localizer = localizer

    def can_say(self):

        if not self.world_model.is_my_number_set():
            return False

        server_time = self.world_model.get_time()
        cycles = int(server_time * 50 + 0.1)
        is_my_turn = (cycles % (NUM_AGENTS * 2) ==
                      (self.world_model.my_number - 1) * 2)
        is_message_valid = (self.said_message.strip() !=
                            "" and self.said_message is not None)

        return is_my_turn and is_message_valid

    def make_say_message(self):
        if self.can_say():
            return "(say " + self.said_message + ")"
        return ""

    def hear(self):
        raise NotImplementedError

    def say(self):
        raise NotImplementedError
