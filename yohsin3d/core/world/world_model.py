from .enums import *

class WorldModel:
    def __init__(self) -> None:
        self.cycle = 0
        self.time = -1.0
        self.gametime = -1.0
        self.opponent_team_name = None

        self.force_resistance_perceptors = {'rf': None, 'lf': None}

        self.playmode = PlayModes.PM_BEFORE_KICK_OFF
        self.last_playmode = PlayModes.PM_GAME_OVER
        self.last_different_playmode = PlayModes.PM_GAME_OVER

        self.position_groundtruth = [0, 0, 0]
        self.orientation_groundtruth = 0
        self.ball_position_groundtruth = [0,0,0]
    
        self.unum = None
        self.unum_set = False
        
        self.current_agent_global_position = None
        self.last_agent_global_position = None
        self.current_agent_global_orientation = None
        self.current_ball_global_position = None
        
        self.side = SIDE_LEFT
        self.side_set = False
        self.fallen = False

        # Simple Visible Objects are Flags, Goal Posts, and Ball
        self.simple_vision_objects = {
                                "F1R": None,
                                "G1L": None,
                                "G2L": None,
                                "F2R": None,
                                "F2L": None,
                                "G1R": None,
                                "G2R": None,
                                "F1L": None,
                                "B": None,
                            }
        
        # Complex Visible Objects includes Lines, PLayers (Body Parts)
        # Each Player is dict like this: {'head': None, 'rlowerarm': None, 'llowerarm': None, 'rfoot': None, 'lfoot': None}
        self.complex_vision_objects = {
            "Yohsin01" : None,
            "Yohsin02" : None,
            "Yohsin03" : None,
            "Yohsin04" : None,
            "Yohsin05" : None,
            "Yohsin06" : None,
            "Yohsin07" : None,
            "Yohsin08" : None,
            "Yohsin09" : None,
            "Yohsin10" : None,
            "Yohsin11" : None,
            
            "Opponent01" : None,
            "Opponent02" : None,
            "Opponent03" : None,
            "Opponent04" : None,
            "Opponent05" : None,
            "Opponent06" : None,
            "Opponent07" : None,
            "Opponent08" : None,
            "Opponent09" : None,
            "Opponent10" : None,
            "Opponent11" : None,
            
            "L" : None  # List of lines

        }
        
        self.hingeJointStates = {
            'hj1': 0.0,  # Neck Yaw   
            'hj2': 0.0,  # Neck Pitch    
            'raj1': 0.0,  # Right Shoulder Pitch
            'raj2': 0.0,  # Right Shoulder Yaw
            'raj3': 0.0,  # Right Arm Roll
            'raj4': 0.0,  # Right Arm Yaw
            'laj1': 0.0,  # Left Shoulder Pitch
            'laj2': 0.0,  # Left Shoulder Yaw
            'laj3': 0.0,  # Left Arm Roll
            'laj4': 0.0,  # Left Arm Yaw
            'rlj1': 0.0,  # Right Hip YawPitch
            'rlj2': 0.0,  # Right Hip Roll
            'rlj3': 0.0,  # Right Hip Pitch
            'rlj4': 0.0,  # Right Knee Pitch
            'rlj5': 0.0,  # Right Foot Pitch
            'rlj6': 0.0,  # Right Foot Roll
            'llj1': 0.0,  # Left Hip YawPitch
            'llj2': 0.0,  # Left Hip Roll
            'llj3': 0.0,  # Left Hip Pitch
            'llj4': 0.0,  # Left Knee Pitch
            'llj5': 0.0,  # Left Foot Pitch
            'llj6': 0.0,
        }

 

        

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

    def get_last_different_playmode(self):
        return self.last_different_playmode

    def set_last_different_playmode(self, last_different_playmode):
        self.last_different_playmode = last_different_playmode

    def get_unum(self):
        return self.unum

    def set_unum(self, unum):
        self.unum = unum

    def get_unum_set(self):
        return self.unum_set

    def set_unum_set(self, unum_set):
        self.unum_set = unum_set

    def set_position_groundtruth(self, new_pos):
        self.position_groundtruth = new_pos
        
    def set_orientation_groundtruth(self, new_orientation):
        self.orientation_groundtruth = new_orientation
        
    def set_ball_position_groundtruth(self, new_pos):
        self.ball_position_groundtruth = new_pos

    def get_side(self):
        return self.side

    def set_side(self, side):
        self.side = side

    def get_side_set(self):
        return self.side_set

    def set_side_set(self, side_set):
        self.side_set = side_set
