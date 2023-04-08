from .body import *
from .world import *
from .localizer import BaseLocalizer
from .network import Parser


class BaseBehavior:

    def __init__(self, start_coordinates=(0, 0), localizer: BaseLocalizer = None) -> None:
        self.start_coordinates = start_coordinates
        self.monitor_msg = ""
        self.initialized = False
        self.init_beamed = False
        self.localizer = localizer

    def initialize(self, team_name):
        self.world_model = WorldModel(team_name)
        self.body_model = BodyModel(self.world_model)

        self.parser = Parser(world_model=self.world_model,
                             body_model=self.body_model)

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
        x, y = self.start_coordinates
        return self.beam_effector(x, y, 0)

    def hj_effector(self, name, rate):
        return "({} {:.2f})".format(name, rate)

    def compose_action(self):
        message = ""
        for effector in EffectorJoints:
            torque = self.body_model.compute_torque(effector)
            effector_name = effector.to_string()
            message += self.hj_effector(effector_name, torque)

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

        self.localizer.update()

        action = ""
        self.act()
        action += self.compose_action()

        return action

    def act(self):
        pass
