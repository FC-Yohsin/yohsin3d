from ...core.common.joints import Joint
from ...core.world import WorldModel
from ...core.body import BodyModel, BodyParts

# Inspired from:
# https://github.com/LARG/utaustinvilla3d/blob/master/behaviors/checkfall.cc

params_t0 = {
    'getup_parms_stateDownInitialWait': 0.5,
    'getup_parms_stateDown3A1': 51.67747278227646,
    'getup_parms_stateDown3L3': 131.7535106037132,
    'getup_parms_stateDown3MinTime': 0.04,
    'getup_parms_stateDown5L1': -45.61543864318751,
    'getup_parms_stateDown5MinTime': 0.9,
    'getup_parms_stateDown7L1': 7.146660948143131,
    'getup_parms_stateDown7L3': 64.86293984615665,
    'getup_parms_stateDown7MinTime': 0.3,
    'getup_parms_stateDown10MinTime': 0.8,
    'getup_parms_stateUpInitialWait': 0.5,
    'getup_parms_stateUp3A1': -137.82661679105144,
    'getup_parms_stateUp3A2': 47.75746255861538,
    'getup_parms_stateUp3A4': 62.08845222070459,
    'getup_parms_stateUp3L3': 20.129514885250764,
    'getup_parms_stateUp3MinTime': 0.2,
    'getup_parms_stateUp5L3': 118.20227245026733,
    'getup_parms_stateUp5MinTime': 0.04,
    'getup_parms_stateUp7L1': -28.310230075504645,
    'getup_parms_stateUp7MinTime': 0.2,
    'getup_parms_stateUp9A1': 46.60215905763356,
    'getup_parms_stateUp9L1': -90.29680084623156,
    'getup_parms_stateUp9L4': -45.66593008367499,
    'getup_parms_stateUp9L5': -47.3966607282542,
    'getup_parms_stateUp9L6': -63.76376603815571,
    'getup_parms_stateUp9MinTime': 0.2,
    'getup_parms_stateUp11A1': 3.592540038790991,
    'getup_parms_stateUp11L1': -60.16186063609875,
    'getup_parms_stateUp11L5': -66.94418816067675,
    'getup_parms_stateUp11MinTime': 0.4,
    'getup_parms_stateUp13A1': -95.06021619327173,
    'getup_parms_stateUp13L1': -27.726371071345866,
    'getup_parms_stateUp13L3': 33.044752335210546,
    'getup_parms_stateUp13L4': -29.541237439782954,
    'getup_parms_stateUp13L5': -26.379841635865372,
    'getup_parms_stateUp13MinTime': 0.04,
    'getup_parms_stateUp15MinTime': 0.6}
params_t1 = {
    'getup_parms_stateDownInitialWait': 0.5,
    'getup_parms_stateDown3A1': 16.568148350107915,
    'getup_parms_stateDown3L3': 113.41133450590875,
    'getup_parms_stateDown3MinTime': 0.04,
    'getup_parms_stateDown5L1': -39.17965858391402,
    'getup_parms_stateDown5MinTime': 0.9,
    'getup_parms_stateDown7L1': -8.232686646848567,
    'getup_parms_stateDown7L3': 62.10471861129633,
    'getup_parms_stateDown7MinTime': 0.3,
    'getup_parms_stateDown10MinTime': 0.8,
    'getup_parms_stateUpInitialWait': 0.5,
    'getup_parms_stateUp3A1': -165.16130968225886,
    'getup_parms_stateUp3A2': 42.58511262180544,
    'getup_parms_stateUp3A4': 117.07281960213916,
    'getup_parms_stateUp3L3': 55.45054826070052,
    'getup_parms_stateUp3MinTime': 0.2,
    'getup_parms_stateUp5L3': 115.49895139205304,
    'getup_parms_stateUp5MinTime': 0.04,
    'getup_parms_stateUp7L1': -68.1166661743677,
    'getup_parms_stateUp7MinTime': 0.2,
    'getup_parms_stateUp9A1': 46.81694893244553,
    'getup_parms_stateUp9L1': -122.97859206412672,
    'getup_parms_stateUp9L4': -37.42441472881181,
    'getup_parms_stateUp9L5': -69.18081712780187,
    'getup_parms_stateUp9L6': -86.80191982495745,
    'getup_parms_stateUp9MinTime': 0.2,
    'getup_parms_stateUp11A1': 42.78745493987175,
    'getup_parms_stateUp11L1': -63.476728163679795,
    'getup_parms_stateUp11L5': -92.55995382987949,
    'getup_parms_stateUp11MinTime': 0.4,
    'getup_parms_stateUp13A1': -50.62380061268099,
    'getup_parms_stateUp13L1': -27.678137746769536,
    'getup_parms_stateUp13L3': 18.485095263513564,
    'getup_parms_stateUp13L4': 14.273184019175599,
    'getup_parms_stateUp13L5': -58.9003662416826,
    'getup_parms_stateUp13MinTime': 0.04,
    'getup_parms_stateUp15MinTime': 0.6}
params_t2 = {
    'getup_parms_stateDownInitialWait': 0.5,
    'getup_parms_stateDown3A1': 47.4610405996882,
    'getup_parms_stateDown3L3': 104.58701666386462,
    'getup_parms_stateDown3MinTime': 0.04,
    'getup_parms_stateDown5L1': -46.16626996041264,
    'getup_parms_stateDown5MinTime': 0.9,
    'getup_parms_stateDown7L1': -8.174758505626324,
    'getup_parms_stateDown7L3': 66.7418834956474,
    'getup_parms_stateDown7MinTime': 0.3,
    'getup_parms_stateDown10MinTime': 0.8,
    'getup_parms_stateUpInitialWait': 0.5,
    'getup_parms_stateUp3A1': -139.74945449732297,
    'getup_parms_stateUp3A2': 39.25063221342788,
    'getup_parms_stateUp3A4': 73.43239538646863,
    'getup_parms_stateUp3L3': 17.86850643399282,
    'getup_parms_stateUp3MinTime': 0.2,
    'getup_parms_stateUp5L3': 123.30024625855616,
    'getup_parms_stateUp5MinTime': 0.04,
    'getup_parms_stateUp7L1': -38.67056678443029,
    'getup_parms_stateUp7MinTime': 0.2,
    'getup_parms_stateUp9A1': 56.9077493498944,
    'getup_parms_stateUp9L1': -99.67874785395259,
    'getup_parms_stateUp9L4': -33.532000140847295,
    'getup_parms_stateUp9L5': -60.93062460878395,
    'getup_parms_stateUp9L6': -70.7774560996261,
    'getup_parms_stateUp9MinTime': 0.2,
    'getup_parms_stateUp11A1': 45.0442618099886,
    'getup_parms_stateUp11L1': -58.43623407729397,
    'getup_parms_stateUp11L5': -93.22374982305332,
    'getup_parms_stateUp11MinTime': 0.4,
    'getup_parms_stateUp13A1': -95.0269318603912,
    'getup_parms_stateUp13L1': -13.040875418712943,
    'getup_parms_stateUp13L3': 48.91105714103771,
    'getup_parms_stateUp13L4': -7.835010869903101,
    'getup_parms_stateUp13L5': -59.141845254226816,
    'getup_parms_stateUp13MinTime': 0.04,
    'getup_parms_stateUp15MinTime': 0.6}
params_t3 = {
    'getup_parms_stateDownInitialWait': 0.5,
    'getup_parms_stateDown3A1': 31.373778672868006,
    'getup_parms_stateDown3L3': 132.04992361431232,
    'getup_parms_stateDown3MinTime': 0.04,
    'getup_parms_stateDown5L1': -40.19865222799057,
    'getup_parms_stateDown5MinTime': 0.9,
    'getup_parms_stateDown7L1': -5.303130226020178,
    'getup_parms_stateDown7L3': 61.27667080700868,
    'getup_parms_stateDown7MinTime': 0.3,
    'getup_parms_stateDown10MinTime': 0.8,
    'getup_parms_stateUpInitialWait': 0.5,
    'getup_parms_stateUp3A1': -74.19212693705215,
    'getup_parms_stateUp3A2': 22.059688990978437,
    'getup_parms_stateUp3A4': -2.805504697930181,
    'getup_parms_stateUp3L3': 28.62816708004984,
    'getup_parms_stateUp3MinTime': 0.2,
    'getup_parms_stateUp5L3': 150.94279526388357,
    'getup_parms_stateUp5MinTime': 0.04,
    'getup_parms_stateUp7L1': -77.42911633035874,
    'getup_parms_stateUp7MinTime': 0.2,
    'getup_parms_stateUp9A1': 7.430718528871051,
    'getup_parms_stateUp9L1': -97.75479706018714,
    'getup_parms_stateUp9L4': -117.6731135265411,
    'getup_parms_stateUp9L5': -56.61496431999153,
    'getup_parms_stateUp9L6': -12.254544769250895,
    'getup_parms_stateUp9MinTime': 0.2,
    'getup_parms_stateUp11A1': -16.438083494272085,
    'getup_parms_stateUp11L1': -140.85938039354576,
    'getup_parms_stateUp11L5': -10.078725855976106,
    'getup_parms_stateUp11MinTime': 0.4,
    'getup_parms_stateUp13A1': -134.62269922433833,
    'getup_parms_stateUp13L1': 4.809371288194855,
    'getup_parms_stateUp13L3': 58.230989205302535,
    'getup_parms_stateUp13L4': -24.26206719200843,
    'getup_parms_stateUp13L5': 1.3567977261284696,
    'getup_parms_stateUp13MinTime': 0.04,
    'getup_parms_stateUp15MinTime': 0.6}
params_t4 = {
    'getup_parms_stateDownInitialWait': 0.5,
    'getup_parms_stateDown3A1': 50.98021756053253,
    'getup_parms_stateDown3L3': 126.1220933612166,
    'getup_parms_stateDown3MinTime': 0.04,
    'getup_parms_stateDown5L1': -48.00207256772667,
    'getup_parms_stateDown5MinTime': 0.9,
    'getup_parms_stateDown7L1': -22.340860939025024,
    'getup_parms_stateDown7L3': 63.33360057004941,
    'getup_parms_stateDown7MinTime': 0.3,
    'getup_parms_stateDown10MinTime': 0.8,
    'getup_parms_stateDown3L7': 10.434125629408747,
    'getup_parms_stateDown5L7': -24.614475691676574,
    'getup_parms_stateDown7L7': -25.565997236105442,
    'getup_parms_stateUpInitialWait': 0.5,
    'getup_parms_stateUp3A1': -160.48868850844917,
    'getup_parms_stateUp3A2': 43.87852475409584,
    'getup_parms_stateUp3A4': 47.107544084593684,
    'getup_parms_stateUp3L3': 15.740604821659796,
    'getup_parms_stateUp3MinTime': 0.2,
    'getup_parms_stateUp5L3': 132.27670902584242,
    'getup_parms_stateUp5MinTime': 0.04,
    'getup_parms_stateUp7L1': -33.46492505628697,
    'getup_parms_stateUp7MinTime': 0.2,
    'getup_parms_stateUp9A1': 35.11715155456652,
    'getup_parms_stateUp9L1': -93.41203497109993,
    'getup_parms_stateUp9L4': -42.02538707170181,
    'getup_parms_stateUp9L5': -74.20809920914384,
    'getup_parms_stateUp9L6': -45.011664557354386,
    'getup_parms_stateUp9MinTime': 0.2,
    'getup_parms_stateUp11A1': 12.335079113997592,
    'getup_parms_stateUp11L1': -59.73823689637007,
    'getup_parms_stateUp11L5': -75.30629507279436,
    'getup_parms_stateUp11MinTime': 0.4,
    'getup_parms_stateUp13A1': -92.92376016195993,
    'getup_parms_stateUp13L1': -19.862994508032,
    'getup_parms_stateUp13L3': 6.715020876796658,
    'getup_parms_stateUp13L4': 9.198657450095972,
    'getup_parms_stateUp13L5': -45.49461773853202,
    'getup_parms_stateUp13MinTime': 0.04,
    'getup_parms_stateUp15MinTime': 0.6,
    'getup_parms_stateUp3L7': -13.906519868066766,
    'getup_parms_stateUp5L7': -13.153693919511753,
    'getup_parms_stateUp7L7': 11.047229348390086,
    'getup_parms_stateUp9L7': -24.75948253132887,
    'getup_parms_stateUp11L7': -47.26657398170224,
    'getup_parms_stateUp13L7': 11.057355562206059}

agent_type_to_params = {
    0: params_t0,
    1: params_t1,
    2: params_t2,
    3: params_t3,
    4: params_t4,
}


class Params:
    def __init__(self, params_dict) -> None:
        self.params_dict = params_dict

    def find(self, key):
        return self.params_dict[key]


class FallRecovery:

    def __init__(self, body_model: BodyModel, world_model: WorldModel) -> None:
        self.fall_state = 0
        self.fallen_left = False
        self.fallen_right = False
        self.fallen_down = False
        self.fallen_up = False
        self.fall_state_start = None
        self.fall_state_end = -1
        self.fall_time_wait = -1

        self.body_model = body_model
        self.world_model = world_model

        self.params = Params(agent_type_to_params[self.body_model.agent_type])

    def detect_fall_and_getup(self):

        accel = self.body_model.get_accel_rates()

        if (self.fall_state == 0):
            # Check if falling. Only one flag is to be set if falling.
            self.fallen_up = (accel[0] < -6.5)
            self.fallen_down = not self.fallen_up and (accel[0] > 7.5)
            self.fallen_right = not self.fallen_up and not self.fallen_down and (
                accel[1] < -6.5)
            self.fallen_left = not self.fallen_up and not self.fallen_down and not self.fallen_right and (
                accel[1] > 6.5)

            if (self.fallen_up or self.fallen_down or self.fallen_left or self.fallen_right):
                self.body_model.update_speed(6)
                self.fall_state = 1
                self.current_fall_state_start_time = -1.0
                self.world_model.set_fallen(True)

            else:
                self.fall_state = 0
                self.world_model.set_fallen(False)
                return False

        # Keep head forward
        self.body_model.set_target_angle(int(Joint.H1), 0)
        self.body_model.set_angle_gain(int(Joint.H1), 0.5)

        if (self.fall_state == 1):

            if (self.current_fall_state_start_time < 0):
                self.current_fall_state_start_time = self.world_model.get_time()

            self.body_model.set_initial_arm(BodyParts.ARM_LEFT)
            self.body_model.set_initial_arm(BodyParts.ARM_RIGHT)
            self.body_model.set_initial_leg(BodyParts.LEG_LEFT)
            self.body_model.set_initial_leg(BodyParts.LEG_RIGHT)

            self.body_model.set_target_angle(int(Joint.LA2), 90)
            self.body_model.set_target_angle(int(Joint.RA2), -90)

            self.body_model.set_target_angle(int(Joint.LA4), 0)
            self.body_model.set_target_angle(int(Joint.RA4), 0)

            if (self.fall_time_wait < 0):
                self.fall_time_wait = self.world_model.get_time()

            if (self.world_model.get_time() -
                    self.current_fall_state_start_time > 0.2):  # TUNE

                self.fall_state = 2
                self.current_fall_state_start_time = -1.0
                self.fall_time_stamp = self.world_model.get_time()
                self.fall_time_wait = -1

        elif (self.fall_state == 2):

            if (self.current_fall_state_start_time < 0):
                self.current_fall_state_start_time = self.world_model.get_time()

            if (
                self.world_model.get_time() > (
                    self.fall_time_stamp + (
                        float(
                            self.params.find("getup_parms_stateDownInitialWait")) if self.fallen_down else float(
                    self.params.find("getup_parms_stateUpInitialWait"))))):
                self.fall_time_stamp = -1
                self.fall_state = 1
                self.current_fall_state_start_time = -1.0

                # Check once again. If still fallen right or left, act as
                # though fallen up.
                self.fallen_up = (accel[0] < -6.5)
                self.fallen_down = not self.fallen_up and (accel[0] > 6.5)
                self.fallen_right = not self.fallen_up and not self.fallen_down and (
                    accel[1] < -6.5)
                self.fallen_left = not self.fallen_up and not self.fallen_down and not self.fallen_right and (
                    accel[1] > 6.5)

                if (self.fallen_up or self.fallen_right or self.fallen_left):
                    self.fallen_up = True
                    self.fallen_right = False
                    self.fallen_left = False
                    self.fall_state = 3
                    self.current_fall_state_start_time = -1.0

                elif (self.fallen_down):
                    self.fall_state = 3
                    self.current_fall_state_start_time = -1.0

                else:  # Magically, we are upnot
                    self.fall_state = 0
                    self.current_fall_state_start_time = -1.0

        # Recovering
        if (self.fallen_down):

            if (self.fall_state == 3):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_target_angle(
                    int(Joint.LA1),
                    float(self.params.find("getup_parms_stateDown3A1")))
                self.body_model.set_target_angle(
                    int(Joint.RA1),
                    float(self.params.find("getup_parms_stateDown3A1")))

                self.body_model.set_target_angle(int(Joint.LA2), 0)
                self.body_model.set_target_angle(int(Joint.RA2), 0)

                self.body_model.set_target_angle(
                    int(Joint.LL3),
                    float(self.params.find("getup_parms_stateDown3L3")))
                self.body_model.set_target_angle(
                    int(Joint.RL3),
                    float(self.params.find("getup_parms_stateDown3L3")))

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateDown3MinTime"))):
                    self.fall_state = 4
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 4):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() > (self.fall_time_stamp + 0)):
                    self.fall_time_stamp = -1
                    self.fall_state = 5
                    self.current_fall_state_start_time = -1.0

            elif (self.fall_state == 5):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_target_angle(
                    int(Joint.LL1),
                    float(self.params.find("getup_parms_stateDown5L1")))
                self.body_model.set_target_angle(
                    int(Joint.RL1),
                    float(self.params.find("getup_parms_stateDown5L1")))

                self.body_model.set_target_angle(int(Joint.LL5), 0)
                self.body_model.set_target_angle(int(Joint.RL5), 0)

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateDown5MinTime"))):
                    self.fall_state = 6
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 6):
                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() > (
                        self.fall_time_stamp + 0.25)):
                    self.fall_time_stamp = -1
                    self.fall_state = 7
                    self.current_fall_state_start_time = -1.0

            elif (self.fall_state == 7):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_target_angle(
                    int(Joint.LL1),
                    float(self.params.find("getup_parms_stateDown7L1")))
                self.body_model.set_target_angle(
                    int(Joint.RL1),
                    float(self.params.find("getup_parms_stateDown7L1")))

                self.body_model.set_target_angle(
                    int(Joint.LL3),
                    float(self.params.find("getup_parms_stateDown7L3")))
                self.body_model.set_target_angle(
                    int(Joint.RL3),
                    float(self.params.find("getup_parms_stateDown7L3")))

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateDown7MinTime"))):
                    self.fall_state = 8
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 8):
                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() > (self.fall_time_stamp + 0)):
                    self.fall_time_stamp = -1
                    self.fall_state = 9
                    self.current_fall_state_start_time = -1.0

            elif (self.fall_state == 9):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_initial_arm(BodyParts.ARM_LEFT)
                self.body_model.set_initial_arm(BodyParts.ARM_RIGHT)
                self.body_model.set_initial_leg(BodyParts.LEG_LEFT)
                self.body_model.set_initial_leg(BodyParts.LEG_RIGHT)

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateDown10MinTime"))):
                    self.fall_state = 10
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 10):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() < (self.fall_time_stamp + 1.0)):
                    gyroRates = self.body_model.get_gyro_rates()
                    # Check for stability and if gyro rates are high don't say
                    # that we have recovered.
                    if (gyroRates[0] > .5 or gyroRates[1] > .5
                            or gyroRates[2] > .5):
                        return True

                if (self.world_model.get_time() > (self.fall_time_stamp + 0.1)):
                    self.fall_time_stamp = -1
                    self.current_fall_state_start_time = -1.0
                    self.fall_state = 0
                    self.fallen_down = False
                    self.last_getup_recovery_time = self.world_model.get_time()
                    # recursive ...
                    return self.detect_fall_and_getup()

        if (self.fallen_up):

            if (self.fall_state == 3):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_target_angle(
                    int(Joint.LA1),
                    float(self.params.find("getup_parms_stateUp3A1")))
                self.body_model.set_target_angle(
                    int(Joint.RA1),
                    float(self.params.find("getup_parms_stateUp3A1")))

                self.body_model.set_target_angle(
                    int(Joint.LA2),
                    float(self.params.find("getup_parms_stateUp3A2")))
                self.body_model.set_target_angle(
                    int(Joint.RA2),
                    -float(self.params.find("getup_parms_stateUp3A2")))

                self.body_model.set_target_angle(
                    int(Joint.LA4),
                    float(self.params.find("getup_parms_stateUp3A4")))
                self.body_model.set_target_angle(
                    int(Joint.RA4),
                    -float(self.params.find("getup_parms_stateUp3A4")))

                self.body_model.set_target_angle(
                    int(Joint.LL3),
                    float(self.params.find("getup_parms_stateUp3L3")))
                self.body_model.set_target_angle(
                    int(Joint.RL3),
                    float(self.params.find("getup_parms_stateUp3L3")))

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateUp3MinTime"))):
                    self.fall_state = 4
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 4):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() > (self.fall_time_stamp + 0)):
                    self.fall_time_stamp = -1
                    self.fall_state = 5
                    self.current_fall_state_start_time = -1.0

            elif (self.fall_state == 5):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_target_angle(
                    int(Joint.LL3),
                    float(self.params.find("getup_parms_stateUp5L3")))
                self.body_model.set_target_angle(
                    int(Joint.RL3),
                    float(self.params.find("getup_parms_stateUp5L3")))

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateUp5MinTime"))):
                    self.fall_state = 6
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 6):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() > (self.fall_time_stamp + 0)):
                    self.fall_time_stamp = -1
                    self.fall_state = 7
                    self.current_fall_state_start_time = -1.0

            elif (self.fall_state == 7):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_target_angle(int(Joint.LA1), 0)
                self.body_model.set_target_angle(int(Joint.RA1), 0)

                self.body_model.set_target_angle(int(Joint.LA2), 0)
                self.body_model.set_target_angle(int(Joint.RA2), 0)

                self.body_model.set_target_angle(
                    int(Joint.LL1),
                    float(self.params.find("getup_parms_stateUp7L1")))
                self.body_model.set_target_angle(
                    int(Joint.RL1),
                    float(self.params.find("getup_parms_stateUp7L1")))

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateUp7MinTime"))):
                    self.fall_state = 8
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 8):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() > (self.fall_time_stamp + 0)):
                    self.fall_time_stamp = -1
                    self.fall_state = 9
                    self.current_fall_state_start_time = -1.0

            elif (self.fall_state == 9):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_target_angle(
                    int(Joint.LA1),
                    float(self.params.find("getup_parms_stateUp9A1")))
                self.body_model.set_target_angle(
                    int(Joint.RA1),
                    float(self.params.find("getup_parms_stateUp9A1")))

                self.body_model.set_target_angle(
                    int(Joint.LL1),
                    float(self.params.find("getup_parms_stateUp9L1")))
                self.body_model.set_target_angle(
                    int(Joint.RL1),
                    float(self.params.find("getup_parms_stateUp9L1")))

                self.body_model.set_target_angle(
                    int(Joint.LL4),
                    float(self.params.find("getup_parms_stateUp9L4")))
                self.body_model.set_target_angle(
                    int(Joint.RL4),
                    float(self.params.find("getup_parms_stateUp9L4")))

                self.body_model.set_target_angle(
                    int(Joint.LL5),
                    float(self.params.find("getup_parms_stateUp9L5")))
                self.body_model.set_target_angle(
                    int(Joint.RL5),
                    float(self.params.find("getup_parms_stateUp9L5")))

                self.body_model.set_target_angle(
                    int(Joint.LL6),
                    float(self.params.find("getup_parms_stateUp9L6")))
                self.body_model.set_target_angle(
                    int(Joint.RL6),
                    -float(self.params.find("getup_parms_stateUp9L6")))

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateUp9MinTime"))):
                    self.fall_state = 10
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 10):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() > (self.fall_time_stamp + 0)):
                    self.fall_time_stamp = -1
                    self.fall_state = 11
                    self.current_fall_state_start_time = -1.0

            elif (self.fall_state == 11):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_target_angle(
                    int(Joint.LA1),
                    float(self.params.find("getup_parms_stateUp11A1")))
                self.body_model.set_target_angle(
                    int(Joint.RA1),
                    float(self.params.find("getup_parms_stateUp11A1")))

                self.body_model.set_target_angle(
                    int(Joint.LL1),
                    float(self.params.find("getup_parms_stateUp11L1")))
                self.body_model.set_target_angle(
                    int(Joint.RL1),
                    float(self.params.find("getup_parms_stateUp11L1")))

                self.body_model.set_target_angle(
                    int(Joint.LL5),
                    float(self.params.find("getup_parms_stateUp11L5")))
                self.body_model.set_target_angle(
                    int(Joint.RL5),
                    float(self.params.find("getup_parms_stateUp11L5")))

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateUp11MinTime"))):
                    self.fall_state = 12
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 12):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() > (self.fall_time_stamp + 0)):
                    self.fall_time_stamp = -1
                    self.fall_state = 13
                    self.current_fall_state_start_time = -1.0

            elif (self.fall_state == 13):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_target_angle(
                    int(Joint.LA1),
                    float(self.params.find("getup_parms_stateUp13A1")))
                self.body_model.set_target_angle(
                    int(Joint.RA1),
                    float(self.params.find("getup_parms_stateUp13A1")))

                self.body_model.set_target_angle(
                    int(Joint.LL1),
                    float(self.params.find("getup_parms_stateUp13L1")))
                self.body_model.set_target_angle(
                    int(Joint.RL1),
                    float(self.params.find("getup_parms_stateUp13L1")))

                self.body_model.set_target_angle(
                    int(Joint.LL3),
                    float(self.params.find("getup_parms_stateUp13L3")))
                self.body_model.set_target_angle(
                    int(Joint.RL3),
                    float(self.params.find("getup_parms_stateUp13L3")))

                self.body_model.set_target_angle(
                    int(Joint.LL4),
                    float(self.params.find("getup_parms_stateUp13L4")))
                self.body_model.set_target_angle(
                    int(Joint.RL4),
                    float(self.params.find("getup_parms_stateUp13L4")))

                self.body_model.set_target_angle(
                    int(Joint.LL5),
                    float(self.params.find("getup_parms_stateUp13L5")))
                self.body_model.set_target_angle(
                    int(Joint.RL5),
                    float(self.params.find("getup_parms_stateUp13L5")))

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                #      if(self.bodyModel.targetsReached()){
                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateUp13MinTime"))):
                    self.fall_state = 14
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 14):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() > (self.fall_time_stamp + 0)):
                    self.fall_time_stamp = -1
                    self.fall_state = 15
                    self.current_fall_state_start_time = -1.0

            elif (self.fall_state == 15):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                self.body_model.set_initial_arm(BodyParts.ARM_LEFT)
                self.body_model.set_initial_arm(BodyParts.ARM_RIGHT)
                self.body_model.set_initial_leg(BodyParts.LEG_LEFT)
                self.body_model.set_initial_leg(BodyParts.LEG_RIGHT)

                if (self.fall_time_wait < 0):
                    self.fall_time_wait = self.world_model.get_time()

                if (self.world_model.get_time() - self.current_fall_state_start_time >
                        float(self.params.find("getup_parms_stateUp15MinTime"))):
                    self.fall_state = 16
                    self.current_fall_state_start_time = -1.0
                    self.fall_time_stamp = self.world_model.get_time()
                    self.fall_time_wait = -1

            elif (self.fall_state == 16):

                if (self.current_fall_state_start_time < 0):
                    self.current_fall_state_start_time = self.world_model.get_time()

                if (self.world_model.get_time() < (self.fall_time_stamp + 1.0)):
                    gyroRates = self.body_model.get_gyro_rates()
                    # Check for stability and if gyro rates are high don't say
                    # that we have recovered.
                    if (gyroRates[0] > .5 or gyroRates[1] > .5
                            or gyroRates[2] > .5):
                        return True

                if (self.world_model.get_time() > (self.fall_time_stamp + 0.1)):
                    self.fall_time_stamp = -1
                    self.fall_state = 0
                    self.current_fall_state_start_time = -1.0
                    self.fallen_up = False
                    self.last_getup_recovery_time = self.world_model.get_time()
                    # recursive ...
                    return self.detect_fall_and_getup()

        return True
