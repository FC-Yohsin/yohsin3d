import re
from typing import List
from ..body import *
from ..world import *
from ..communicator import *
from .constants import *
from ..common import perceptor_to_joint


class Parser:

    def __init__(self,
                 world_model,
                 body_model,
                 communicator,
                 ) -> None:

        self.world_model: WorldModel = world_model
        self.body_model: BodyModel = body_model
        self.communicator: BaseCommunicator = communicator

        self.side = Sides.LEFT

    def tokenise(self, s) -> List[str]:
        string = re.sub(r'[\(\)]', ' ', s)
        result = re.split(r'\s+', string.strip())
        return result

    def __parser_helper(self, matching_string, string):
        match = re.search(fr'{matching_string}\s+([^\)\]]+)', string)
        if match:
            return match.group(1)

    def __parse_time(self, string):
        time = float(self.__parser_helper("now", string))
        self.world_model.set_time(time)
        self.world_model.increment_cycle()
        return time is not None

    def __parse_game_state(self, string):

        playmode_string = self.__parser_helper("pm", string)
        playmode = PlayModes(playmode_string)
        self.world_model.set_last_playmode(self.world_model.get_playmode())
        self.world_model.set_playmode(playmode)

        gametime = float(self.__parser_helper("t", string))
        self.world_model.set_gametime(gametime)

        if self.world_model.get_my_number() is None:
            unum = (self.__parser_helper("unum", string))
            self.world_model.set_my_number(int(unum) if unum else None)

        score_left = int(self.__parser_helper("sl", string))
        self.world_model.set_score_left(score_left)

        score_right = int(self.__parser_helper("sr", string))
        self.world_model.set_score_right(score_right)

        if not self.world_model.is_side_set():
            side = self.__parser_helper("team", string)
            if side is not None:
                self.world_model.set_side(
                    Sides.LEFT if side == "left" else Sides.RIGHT)

        return True

    def __parse_gyro(self, string):
        rateX, rateY, rateZ = self.__get_xyz(string, "rt")
        self.body_model.set_gyro_rates((rateX, rateY, rateZ))
        return True

    def __get_xyz(self, string, start):
        x, y, z = self.__parser_helper(start, string).split()
        return float(x), float(y), float(z)

    def __parse_accelerometer(self, string):
        rateX, rateY, rateZ = self.__get_xyz(string, "a")

        # Sometimes spurious (very high or NaN) readings come through. Clip
        # them.
        spuriousThreshold = 20.0
        if ((abs(rateX) > spuriousThreshold)):
            rateX = 0

        if ((abs(rateY) > spuriousThreshold)):
            rateY = 0

        if ((abs(rateZ) > spuriousThreshold)):
            rateZ = 0

        #  Make signs compatible with agent's local axes.
        correctedRateX = -rateY
        correctedRateY = rateX
        correctedRateZ = -rateZ

        #  Apply filter to raw accelerometer data
        K = 0.9
        lastAccel = self.body_model.get_accel_rates()
        correctedRateX = K * lastAccel[0] + (1 - K) * correctedRateX
        correctedRateY = K * lastAccel[1] + (1 - K) * correctedRateY
        correctedRateZ = K * lastAccel[2] + (1 - K) * correctedRateZ

        self.body_model.set_accel_rates(
            (correctedRateX, correctedRateY, correctedRateZ))

    def __segment(self, string):
        return re.findall(
            r'\(([^()]*(?:\(([^()]*(?:\((?:[^()]*(?:\([^()]*\)[^()]*)*)\)[^()]*)*)\)[^()]*)*)\)',
            string)

    def __parse_hinge_joint(self, string):
        effector_name = perceptor_to_joint[self.__parser_helper("n", string)]
        effector_angle = float(self.__parser_helper("ax", string))

        self.body_model.set_current_angle(effector_name, effector_angle)
        return True

    def __parse_FRP(self, str):
        name = self.__parser_helper("n", str)
        centreX, centreY, centreZ = self.__get_xyz(str, "c")
        forceX, forceY, forceZ = self.__get_xyz(str, "f")
        name = ForceResistancePerceptors(name)
        self.world_model.force_resistance_perceptors[name] = [
            (centreX, centreY, centreZ), (forceX, forceY, forceZ)]
        return True

    def __get_first(self, string):
        return re.search(r'^[^( ]+', string).group(0)

    def __parse_simple_vision_object(self, string):
        name = self.__get_first(string)
        x, y, z = self.__get_xyz(string, "pol")
        name = VisibleObjects(name)
        self.world_model.simple_vision_objects[name] = (x, y, z)
        return True

    def __parse_line(self, string):
        '''
        Parse Line is not complete yet. There are multiple lines data coming from the server. We need to figure out how to
        process that.

        TODO: Need to undderstand the concept of the lines
        '''
        tokens = self.tokenise(string)

        r = float(tokens[2])
        theta = float(tokens[3])
        phi = float(tokens[4])

        r2 = float(tokens[6])
        theta2 = float(tokens[7])
        phi2 = float(tokens[8])

        self.world_model.lines = [(r, theta, phi), (r2, theta2, phi2)]
        return True

    def __parse_player(self, string):

        valid = False

        tokens = self.tokenise(string)
        # based on the assumption that the max characters in a team name will
        # be 100
        valid = (len(tokens) == 30)

        if valid:
            agent_num = (tokens[4]).zfill(2)
            team_name = tokens[2]

            agent_num = int(agent_num)

            player_info = {
                "head": (float(tokens[7]), float(tokens[8]), float(tokens[9])),
                "rlowerarm": (float(tokens[12]), float(tokens[13]), float(tokens[14])),
                "llowerarm": (float(tokens[17]), float(tokens[18]), float(tokens[19])),
                "rfoot": (float(tokens[22]), float(tokens[23]), float(tokens[24])),
                "lfoot": (float(tokens[27]), float(tokens[28]), float(tokens[29]))
            }

            if team_name == self.world_model.my_team_name:
                self.world_model.teammate_info[agent_num].is_visible = True
                self.world_model.teammate_info[agent_num].update_from_dict(
                    player_info)
            else:
                self.world_model.opponent_info[agent_num].is_visible = True
                self.world_model.opponent_info[agent_num].update_from_dict(
                    player_info)

        return valid

    def __reset_simple_non_visible_objects(self, string):
        for object in VisibleObjects:
            if not re.search(f"[(]{object.value}\\s", string):
                self.world_model.simple_vision_objects[object] = None

    def __is_player_visible(self, string, num, team):
        regex = f"\\(P\\s+\\(team\\s+{team}\\)\\s+\\(id\\s+{num}\\)"
        return re.search(regex, string) is not None

    def __reset_player_information(self, string):
        for object in self.world_model.teammate_info.keys():
            if not self.__is_player_visible(
                    string, object, self.world_model.my_team_name):
                self.world_model.teammate_info[object].is_visible = False

        for object in self.world_model.opponent_info.keys():
            if not self.__is_player_visible(
                    string, object, self.world_model.opponent_team_name):
                self.world_model.opponent_info[object].is_visible = False

    def __parse_position_groundtruth(self, string):
        tokens = self.tokenise(string)
        self.world_model.set_position_groundtruth(
            (float(tokens[1]), float(tokens[2]), float(tokens[3])))

    def __parse_orientation_groundtruth(self, string):
        tokens = self.tokenise(string)
        self.world_model.set_orientation_groundtruth(float(tokens[1]))

    def __parse_ball_position_groundtruth(self, string):
        tokens = self.tokenise(string)
        self.world_model.set_ball_position_groundtruth(
            (float(tokens[1]), float(tokens[2]), float(tokens[3])))

    def __parse_see(self, string):
        valid = True

        self.__reset_simple_non_visible_objects(string=string)
        self.__reset_player_information(string=string)

        str_segments = self.__segment(string)

        for segment in str_segments:
            segment: str = segment[0].strip()

            # Goalpost
            if (segment[0] == 'G'):
                valid = self.__parse_simple_vision_object(segment) and valid

            # Flags
            elif (segment[0] == 'F'):
                valid = self.__parse_simple_vision_object(segment) and valid

            # Ball
            elif (segment[0] == 'B'):
                valid = self.__parse_simple_vision_object(segment) and valid

            # Player
            elif (segment[0] == 'P'):
                self.__parse_player(segment)

            # My Position and My Orientation (Ground Truth)
            elif (segment[0] == 'm'):
                if (segment[:6].strip() == 'mypos'):
                    self.__parse_position_groundtruth(segment)

                if (segment[:8].strip() == 'myorien'):
                    self.__parse_orientation_groundtruth(segment)

            # GroundTruth Ball Position
            elif (segment[0] == 'b'):
                if (segment[:8].strip() == 'ballpos'):
                    self.__parse_ball_position_groundtruth(segment)

            # See token (ignore)
            elif (segment[0] == 'S'):
                pass

            # Line
            elif (segment[0] == 'L'):
                valid = self.__parse_line(segment)

            else:
                valid = False

        return valid

    def __parse_hear(self: 'Parser', string):

        tokens = self.tokenise(string)
        valid = False

        heard_time = 0.0
        is_self = False
        message = ""

        valid = len(tokens) == 5

        if not valid:
            return valid

        i = 1

        if len(tokens) == 5:
            team = tokens[i]
            i += 1
            if team != self.world_model.my_team_name:
                self.world_model.opponent_team_name = team
                return True

        heard_time = float(tokens[i])

        if tokens[i + 1] == "self":
            is_self = True
        else:
            is_self = False

        i += 2

        if i >= len(tokens):
            return False

        message = tokens[i]
        delta_game_time = self.world_model.get_time() - self.world_model.get_gametime()
        hear_game_time = heard_time + delta_game_time
        orientation = tokens[3]

        self.communicator.heard_message.update(
            message=message,
            heard_time=hear_game_time,
            team_name=team,
            voice_orientation=orientation
        )

        return valid

    def parse(self, string):

        valid = True

        inputSegments = self.__segment(string)

        for segment in inputSegments:
            segment: str = segment[0].strip()

            # Time
            if (segment[0] == 't'):
                valid = self.__parse_time(segment) and valid

            elif (segment[0] == 'G'):
                # GameState
                if (segment[1] == 'S'):
                    valid = self.__parse_game_state(segment) and valid

                # Gyro
                else:
                    valid = self.__parse_gyro(segment) and valid

            # Hear #TODO
            elif (segment[0] == 'h'):
                valid = self.__parse_hear(segment) and valid

            # Hinge Joint
            elif (segment[0] == 'H'):
                valid = self.__parse_hinge_joint(segment) and valid

            # See
            elif (segment[0] == 'S'):
                valid = self.__parse_see(segment)

            # FRP
            elif (segment[0] == 'F'):
                valid = self.__parse_FRP(segment) and valid

            # Accelerometer
            elif (segment[0] == 'A'):
                valid = self.__parse_accelerometer(segment) and valid

            else:
                valid = False

        return True
