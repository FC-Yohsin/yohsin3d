from .enums import *
from ..common import GroundTruthModel


class WorldModel:
    def __init__(self, teamname) -> None:
        self.cycle = 0
        self.time = -1.0
        self.gametime = -1.0

        self.my_team_name = teamname
        self.opponent_team_name = None

        self.force_resistance_perceptors = {
            ForceResistancePerceptors.RF: None,
            ForceResistancePerceptors.LF: None
        }

        self.playmode = PlayModes.BEFORE_KICK_OFF
        self.last_playmode = PlayModes.GAME_OVER

        self.groundtruth: GroundTruthModel = GroundTruthModel()

        self.my_number = None
        self.side = Sides.LEFT
        self.fallen = False

        self.simple_vision_objects = {key: None for key in VisibleObjects}
        self.teammate_info = {player: PlayerInfo() for player in range(1, 12)}
        self.opponent_info = {player: PlayerInfo() for player in range(1, 12)}

        # Need to see the concept of lines
        self.lines = None

        self.score_left = None
        self.score_right = None

    def is_fallen(self):
        return self.fallen

    def set_fallen(self, fallen):
        self.fallen = fallen

    def getCycle(self):
        return self.cycle

    def increment_cycle(self):
        self.cycle += 1

    def set_cycle(self, cycle):
        self.cycle = cycle

    def get_score_left(self):
        return self.score_left

    def set_score_left(self, score_left):
        self.score_left = score_left

    def get_score_right(self):
        return self.score_right

    def set_score_right(self, score_right):
        self.score_right = score_right

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = float(time)

    def get_gametime(self):
        return self.gametime

    def set_gametime(self, gametime):
        self.gametime = float(gametime)

    def get_playmode(self):
        return self.playmode

    def set_playmode(self, playmode):
        self.playmode = playmode

    def get_last_playmode(self):
        return self.last_playmode

    def set_last_playmode(self, last_playmode):
        self.last_playmode = last_playmode

    def get_my_number(self):
        return self.my_number

    def set_my_number(self, num):
        self.my_number = num

    def is_my_number_set(self):
        return self.my_number is not None

    def set_position_groundtruth(self, new_pos):
        self.groundtruth.my_location.update_position(new_pos)

    def set_orientation_groundtruth(self, new_orientation):
        self.groundtruth.my_location.update_orientation(new_orientation)

    def set_ball_position_groundtruth(self, new_pos):
        self.groundtruth.ball_position = new_pos

    def get_side(self):
        return self.side

    def set_side(self, side):
        self.side = side

    def is_side_set(self):
        return self.side is not None


class PlayerInfo:
    def __init__(
            self,
            head=None,
            rlowerarm=None,
            llowerarm=None,
            rfoot=None,
            lfoot=None):
        self.head = head
        self.rlowerarm = rlowerarm
        self.llowerarm = llowerarm
        self.rfoot = rfoot
        self.lfoot = lfoot

        self.is_visible = False

    def update_from_dict(self, dict):
        self.head = dict['head']
        self.rlowerarm = dict['rlowerarm']
        self.llowerarm = dict['llowerarm']
        self.rfoot = dict['rfoot']
        self.lfoot = dict['lfoot']
