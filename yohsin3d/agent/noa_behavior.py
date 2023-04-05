from body_model import BodyModel
from world_model import WorldModel
from constants import *
from parser import Parser


class NaoBehavior:

    def __init__(self, team_name: str, rsg: str, agent_unum=0, agent_type=None, start_coordinates=None,) -> None:
        self.rsg = rsg
        self.team_name = team_name
        self.agent_unum = agent_unum
        self.mon_msg = ""
        self.spawn_init = False
        self.initialized = False
        self.init_beamed = False
        if start_coordinates is None:
            self.start_coordinates = (BEFORE_KICKOFF_FORMATION_LEFT[self.agent_unum][0], BEFORE_KICKOFF_FORMATION_LEFT[self.agent_unum][1], 0)
        else:
            self.start_coordinates = start_coordinates


        self.world_model.agent_starting_position = self.start_coordinates
        self.respawning = False


    def spawn_message(self):
        print("Loading rsg: " + "(scene " + self.rsg + ")")
        return f"(scene {self.rsg})"

    def beamable_playmode(self):
        pm = self.world_model.get_playmode()
        return pm == PlayModes.PM_BEFORE_KICK_OFF or pm == PlayModes.PM_GOAL_LEFT or pm == PlayModes.PM_GOAL_RIGHT


    def beam_effector(self, x, y, z):
        return f"(beam {x} {y} {z})"

    def init_beam_effector(self):
        x, y, z = self.start_coordinates
        return self.beam_effector(x, y, z)

    def hj_effector(self, name, rate):
        return "({} {:.2f})".format(name, rate)

    def compose_action(self):
        message = ""
        for effector in EffectorJoints:
            torque = self.body_model.compute_torque(effector)
            effector_name = effector_to_string[effector]
            message += self.hj_effector(effector_name, torque)

        return message

    def get_mon_message(self):
        ret = self.mon_msg
        self.mon_msg = ""
        return ret

    def set_mon_message(self, msg):
        self.mon_msg = msg

    def respawn(self):
        self.init_beamed = False
        self.initialized = False

    def initialize_body(self):
        self.body_model.set_initial_arm(BodyParts.ARM_LEFT)
        self.body_model.set_initial_arm(BodyParts.ARM_RIGHT)
        self.body_model.set_initial_leg(BodyParts.LEG_LEFT)
        self.body_model.set_initial_leg(BodyParts.LEG_RIGHT)
        self.body_model.set_initial_head()

    def spawn_nao(self):
        self.time_when_spawned = (self.world_model.get_time())
        self.spawn_init = True
        msg = "(playMode BeforeKickOff)"
        self.set_mon_message(msg)
        return f"(init (unum {self.agent_unum})(teamname {self.team_name}))"

    def initialize_nao(self):
        
        if not self.world_model.get_unum_set(
        ) or not self.world_model.get_side_set():
            return None

        if not self.init_beamed:
            self.init_beamed = True
            return self.init_beam_effector()
        else:
            self.initialized = True
            return None


    def think(self, message: str) -> str:

        parse_success = self.parser.parse(message)

        if not parse_success:
            print("Parser failed to parse message..")

        if not self.spawn_init:
            return self.spawn_nao()

        if not self.initialized:
            message = self.initialize_nao()
            if message is not None:
                return message

        if self.respawning:
            self.respawning = False
            self.respawn()
        
        action = ""

        self.act()

        action += self.compose_action()

        return action

    def act(self):
        if not self.get_up_utility.detect_fall_and_getup():
            self.left_kick.perform(self.body_model, self.world_model)
            if self.left_kick.is_finished():
                self.left_kick.reset()
