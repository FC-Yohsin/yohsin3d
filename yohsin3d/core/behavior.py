from .body import *
from .world import *
from .localizer import BaseLocalizer
from .network import Parser
from .communicator import BaseCommunicator
from .common import AgentLocation, Joint


class BaseBehavior:

    def __init__(
            self,
            beam_location: AgentLocation,
            localizer: BaseLocalizer = None,
            communicator: BaseCommunicator = None) -> None:
        self.beam_location = beam_location
        self.monitor_msg = ""
        self.initialized = False
        self.init_beamed = False
        self.localizer: BaseLocalizer = localizer
        self.communicator: BaseCommunicator = communicator

    def initialize(self, team_name):
        self.world_model = WorldModel(team_name)
        self.body_model = BodyModel(self.world_model)

        self.parser = Parser(world_model=self.world_model,
                             body_model=self.body_model,
                             communicator=self.communicator
                             )

        if self.communicator is not None:
            self.communicator.initialize(self.world_model, self.localizer)

        if self.localizer is not None:
            self.localizer.initialize(self.world_model)

    def can_rebeam(self):
        pm = self.world_model.get_playmode()
        last_pm = self.world_model.get_last_playmode()
        beamable_modes = [
            PlayModes.BEFORE_KICK_OFF,
            PlayModes.GOAL_LEFT,
            PlayModes.GOAL_RIGHT,
        ]
        return pm in beamable_modes and pm != last_pm

    def beam_effector(self, x, y, z):
        return f"(beam {x} {y} {z})"

    def init_beam_effector(self):
        x, y = self.beam_location.position
        return self.beam_effector(x, y, self.beam_location.orientation)

    def hj_effector(self, name, rate):
        return "({} {:.2f})".format(name, rate)

    def compose_action(self):
        message = ""
        for joint in Joint:
            torque = self.body_model.compute_torque(joint)
            joint_name = joint.effector_name
            message += self.hj_effector(joint_name, torque)

        if self.communicator is not None:
            message += self.communicator.make_say_message()

        return message

    def get_monitor_message(self):
        ret = self.monitor_msg
        self.monitor_msg = ""
        return ret

    def set_monitor_message(self, msg):
        self.monitor_msg = msg

    def initialize_body(self):
        self.body_model.set_initial_arm(BodyParts.ARM_LEFT)
        self.body_model.set_initial_arm(BodyParts.ARM_RIGHT)
        self.body_model.set_initial_leg(BodyParts.LEG_LEFT)
        self.body_model.set_initial_leg(BodyParts.LEG_RIGHT)
        self.body_model.set_initial_head()

    def __can_initialize(self):
        return self.world_model.is_my_number_set() and self.world_model.is_side_set()

    def initialize_nao(self):

        if not self.init_beamed:
            self.init_beamed = True
            return self.init_beam_effector()

        if not self.__can_initialize() or self.initialized:
            return

        self.initialize_body()
        self.initialized = True
        return None

    def think(self, message: str) -> str:

        parse_success = self.parser.parse(message)
        if not parse_success:
            print("Parser failed to parse message..")

        message = self.initialize_nao()
        if message is not None:
            return message

        if self.can_rebeam():
            self.init_beamed = False

        if self.localizer is not None:
            self.localizer.update()

        action = ""
        self.act()

        if self.communicator is not None:
            self.communicator.say()
            self.communicator.hear()

        action += self.compose_action()
        return action

    def act(self):
        raise NotImplementedError
