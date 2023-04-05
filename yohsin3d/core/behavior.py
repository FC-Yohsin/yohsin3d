from .body.body_model import *
from .world.world_model import *
from .network.parser import Parser

class Behavior:

    def __init__(self, team_name: str, rsg: str, agent_unum, agent_type, start_coordinates) -> None:
        self.rsg = rsg
        self.team_name = team_name
        self.agent_unum = agent_unum
        self.start_coordinates = start_coordinates

        self.monitor_msg = ""
        self.spawn_init = False
        self.initialized = False
        self.init_beamed = False
        self.respawning = False

        self.world_model = WorldModel()
        self.body_model = BodyModel(self.world_model)

        self.parser = Parser(world_model=self.world_model,
                             body_model=self.body_model)

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
            effector_name = effector.to_string()
            message += self.hj_effector(effector_name, torque)

        return message

    def get_monitor_message(self):
        ret = self.monitor_msg
        self.monitor_msg = ""
        return ret

    def set_monitor_message(self, msg):
        self.monitor_msg = msg

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
        self.set_monitor_message(msg)
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
       pass
    
