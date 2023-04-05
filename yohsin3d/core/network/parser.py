import re
from typing import List
from ..body.body_model import *
from ..world.world_model import *

class Parser:

    def __init__(self,
                 world_model=None,
                 body_model=None,
                 team_name="test") -> None:

        self.world_model: WorldModel = world_model
        self.body_model: BodyModel = body_model
        self.side = SIDE_LEFT
        self.team_name = team_name


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
        playmode = playModeStringToEnum.get(playmode_string, None)
        self.world_model.set_playmode(playmode)

        gametime = float(self.__parser_helper("t", string))
        self.world_model.set_gametime(gametime)

        if self.world_model.get_unum() is None:
            unum = (self.__parser_helper("unum", string))
            self.world_model.set_unum(int(unum) if unum else None)
            self.world_model.set_unum_set(True)

        score_left = int(self.__parser_helper("sl", string))
        self.world_model.set_score_left(score_left)

        score_right = int(self.__parser_helper("sr", string))
        self.world_model.set_score_right(score_right)

        if not self.world_model.get_side_set():
            side = self.__parser_helper("team", string)
            if side is not None:
                self.world_model.set_side(SIDE_LEFT if side == "left" else SIDE_RIGHT)
                self.world_model.set_side_set(True)

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

        #  Sometimes spurious (very high or NaN) readings come through. Clip them.
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

        self.body_model.set_accel_rates((correctedRateX, correctedRateY, correctedRateZ))


    def __segment(self, string):
        return re.findall(r'\(([^()]*(?:\(([^()]*(?:\((?:[^()]*(?:\([^()]*\)[^()]*)*)\)[^()]*)*)\)[^()]*)*)\)', string)


    def __parse_hinge_joint(self, string):
        effector_name = joint_to_effector[self.__parser_helper("n", string)]
        effector_angle = float(self.__parser_helper("ax", string))
        
        self.body_model.set_current_angle(effector_name, effector_angle)
        return True


    def __parse_FRP(self, str):
        name = self.__parser_helper("n", str)
        centreX, centreY, centreZ = self.__get_xyz(str, "c")
        forceX, forceY, forceZ = self.__get_xyz(str, "f")
        self.world_model.force_resistance_perceptors[name] = [(centreX, centreY, centreZ),(forceX, forceY, forceZ)]
        return True

    def __get_first(self, string):
        return re.search(r'^[^( ]+', string).group(0)


    def __parse_simple_vision_object(self, string):
        name = self.__get_first(string)
        x, y, z = self.__get_xyz(string, "pol")
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

        self.world_model.complex_vision_objects['L'] = [(r, theta, phi), (r2, theta2, phi2)]
        return True


    def __parse_player(self, string):

        valid = False

        tokens = self.tokenise(string)
        valid = (len(tokens) == 30) # based on the assumption that the max characters in a team name will be 100

        if valid:
            agent_num = (tokens[4]).zfill(2)
            team_name = tokens[2]

            player_info = {
                    "head" : (float(tokens[7]), float(tokens[8]), float(tokens[9])),
                    "rlowerarm" : (float(tokens[12]), float(tokens[13]), float(tokens[14])),
                    "llowerarm" : (float(tokens[17]), float(tokens[18]), float(tokens[19])),
                    "rfoot" : (float(tokens[22]), float(tokens[23]), float(tokens[24])),
                    "lfoot" : (float(tokens[27]), float(tokens[28]), float(tokens[29]))
                }

            if team_name == "FC-Yohsin":
                self.world_model.complex_vision_objects[f"Yohsin{agent_num}"] = player_info
            else:
                self.world_model.complex_vision_objects[f"Opponent{agent_num}"] = player_info

        return valid


    def __reset_simple_non_visible_objects(self, string):
        '''
        This method resets the objects to None if they are not visible to the agent based on our latest message from the server
        '''

        for object in self.world_model.simple_vision_objects.keys():
            if not re.search(f"[(]{object}\s", string):
                self.world_model.simple_vision_objects[object] = None


    def __reset_complex_non_visible_objects(self, string):
        '''
        This method resets the objects to None if they are not visible to the agent based on our latest message from the server
        '''

        for object in self.world_model.complex_vision_objects.keys():

            if "FC-Yohsin" in object:
                if not re.search(f"\(P\s\(team\sFC-Yohsin\s[(]id\s{int(object[len(object)-2:])}\)", string):
                    self.world_model.complex_vision_objects[object] = None
            elif "Opponent" in object:
                if not re.search(f"\(P\s\(team\s.{1,100}\)\s\(id\s{int(object[len(object)-2:])}", string):
                    self.world_model.complex_vision_objects[object] = None
            else:
                if not re.search("\(L\s", string):
                    self.world_model.complex_vision_objects["L"] : None





    def __parse_position_groundtruth(self, string):
        tokens = self.tokenise(string)
        self.world_model.set_position_groundtruth((float(tokens[1]), float(tokens[2]), float(tokens[3])))

    def __parse_orientation_groundtruth(self, string):
        tokens = self.tokenise(string)
        self.world_model.set_orientation_groundtruth(float(tokens[1]))

    def __parse_ball_position_groundtruth(self, string):
        tokens = self.tokenise(string)
        self.world_model.set_ball_position_groundtruth((float(tokens[1]), float(tokens[2]), float(tokens[3])))

    def __parse_see(self, string):
        valid = True

        self.__reset_simple_non_visible_objects(string=string)
        self.__reset_complex_non_visible_objects(string=string)

        str_segments = self.__segment(string)

        for segment in str_segments:
            segment:str = segment[0].strip()

            # Goalpost
            if(segment[0] == 'G'):
                valid = self.__parse_simple_vision_object(segment) and valid

            # Flags
            elif(segment[0] == 'F'):
                valid = self.__parse_simple_vision_object(segment) and valid

            # Ball
            elif(segment[0] == 'B'):
                valid = self.__parse_simple_vision_object(segment) and valid

            # Player
            elif(segment[0]== 'P'):
                self.__parse_player(segment)

            # My Position and My Orientation (Ground Truth)
            elif (segment[0]== 'm'):
                if (segment[:6].strip()== 'mypos'):
                    self.__parse_position_groundtruth(segment)

                if (segment[:8].strip() == 'myorien'):
                    self.__parse_orientation_groundtruth(segment)


            # GroundTruth Ball Position
            elif (segment[0]== 'b'):
                if (segment[:8].strip() == 'ballpos'):
                    self.__parse_ball_position_groundtruth(segment)

            # See token (ignore)
            elif  (segment[0]== 'S'):
                pass

            # Line
            elif (segment[0] == 'L' ):
                valid = self.__parse_line(segment)

            else:
                valid = False


        return valid



    def parse(self, string):
        valid = True

        inputSegments = self.__segment(string)

        for segment in inputSegments:
            segment: str = segment[0].strip()

            # Time
            if (segment[0]== 't'):
                valid = self.__parse_time(segment) and valid


            elif(segment[0] == 'G'):
                # GameState
                if(segment[1] == 'S'):
                    valid = self.__parse_game_state(segment) and valid

                # Gyro
                else:
                    valid = self.__parse_gyro(segment) and valid

            # Hear #TODO
            elif(segment[0] == 'h'):
                pass

            # Hinge Joint
            elif(segment[0] == 'H'):
                valid = self.__parse_hinge_joint(segment) and valid


            # See
            elif(segment[0] == 'S'):
                valid = self.__parse_see(segment)

            # FRP
            elif(segment[0] == 'F'):
                valid = self.__parse_FRP(segment) and valid

            # Accelerometer
            elif(segment[0] == 'A'):
                valid = self.__parse_accelerometer(segment) and valid

            else:
                valid = False

        return True