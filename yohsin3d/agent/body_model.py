from world_model import WorldModel
from constants import *
from enums import *
import math


class NaoJoint:
    def __init__(
        self,
        min_angle: float = 0,
        max_angle: float = 0,
        error_tolerance: float = 0,
    ):
        self.min_angle = min_angle
        self.max_angle = max_angle

        self.current_angle = 0
        self.target_angle = 0

        self.error_tolerance = error_tolerance

        self.scale = 1.0

    def set_target_angle(self, angle):

        if (angle < self.min_angle):
            self.target_angle = self.min_angle

        elif (angle > self.max_angle):
            self.target_angle = self.max_angle

        else:
            self.target_angle = angle

    def update(self, angle):
        self.current_angle = angle


class BodyModel:
    def __init__(self, worldModel: WorldModel, agent_type: int) -> None:
        self.agent_type = agent_type
        self.gyro_rates = (0, 0, 0)
        self.prev_gyro_rates = (0, 0, 0)
        self.accel_rates = (0, 0, 0)
        self.walk_angle = None

        self.worldModel = worldModel
        self.joints_list: list[NaoJoint] = [
            None for _ in range(len(EffectorJoints))
        ]
        
        self.previous_joints_list: list[NaoJoint] = [
            None for _ in range(len(EffectorJoints))
        ]
        
        self.initialise_effectors()

    def set_initial_head(self):

        self.set_target_angle(EffectorJoints.EFF_H1, 0)
        self.set_target_angle(EffectorJoints.EFF_H2, -45)

    def target_reached(self, effector_id):
        return abs(self.joints_list[effector_id].current_angle -
                   self.joints_list[effector_id].target_angle
                   ) < self.joints_list[effector_id].error_tolerance

    def set_initial_arm(self, arm) -> bool:

        ang1 = -50.0
        ang2 = 30.0
        ang3 = 0
        ang4 = -50.0

        if (arm == BodyParts.ARM_LEFT):

            self.set_target_angle(EffectorJoints.EFF_LA1, ang1)
            self.set_target_angle(EffectorJoints.EFF_LA2, ang2)
            self.set_target_angle(EffectorJoints.EFF_LA3, ang3)
            self.set_target_angle(EffectorJoints.EFF_LA4, ang4)

        else:  # ARM_RIGHT

            self.set_target_angle(EffectorJoints.EFF_RA1, ang1)
            self.set_target_angle(EffectorJoints.EFF_RA2, -ang2)
            self.set_target_angle(EffectorJoints.EFF_RA3, -ang3)
            self.set_target_angle(EffectorJoints.EFF_RA4, -ang4)

    def set_initial_leg(self, leg) -> bool:

        ang1 = 0
        ang2 = 6.0
        ang3 = 18.0
        ang4 = -30.0
        ang5 = 18.0
        ang6 = -6.0

        if (leg == BodyParts.LEG_LEFT):

            self.set_target_angle(EffectorJoints.EFF_LL1, ang1)
            self.set_target_angle(EffectorJoints.EFF_LL2, ang2)
            self.set_target_angle(EffectorJoints.EFF_LL3, ang3)
            self.set_target_angle(EffectorJoints.EFF_LL4, ang4)
            self.set_target_angle(EffectorJoints.EFF_LL5, ang5)
            self.set_target_angle(EffectorJoints.EFF_LL6, ang6)

        else:

            self.set_target_angle(EffectorJoints.EFF_RL1, ang1)
            self.set_target_angle(EffectorJoints.EFF_RL2, -ang2)
            self.set_target_angle(EffectorJoints.EFF_RL3, ang3)
            self.set_target_angle(EffectorJoints.EFF_RL4, ang4)
            self.set_target_angle(EffectorJoints.EFF_RL5, ang5)
            self.set_target_angle(EffectorJoints.EFF_RL6, -ang6)

    def set_current_angle(self, effector_id, angle):
        self.previous_joints_list[effector_id] = self.joints_list[effector_id].current_angle
        self.joints_list[effector_id].current_angle = angle

    def gettarget_angle(self, effector_id):
        return self.joints_list[effector_id].target_angle

    def update_speed(self, gain):
        for effector in EffectorJoints:
            self.set_angle_gain(effector, gain)

    def get_change_in_gyro_rate(self):
        return (self.gyro_rates[0] - self.prev_gyro_rates[0], 
                self.gyro_rates[1] - self.prev_gyro_rates[1], 
                self.gyro_rates[2] - self.prev_gyro_rates[2])

    def get_change_in_angle(self, effector_id):
        return self.joints_list[effector_id].current_angle - self.previous_joints_list[effector_id]

    def set_target_angle(self, effector_id, angle, gain=None):
        self.joints_list[effector_id].set_target_angle(angle)
        if gain is not None:
            self.set_angle_gain(effector_id, gain)

    def increase_target_angle(self, effector_id, angle_increase, gain=None):
        self.joints_list[effector_id].set_target_angle(
            self.joints_list[effector_id].target_angle + angle_increase)

        if gain is not None:
            self.set_angle_gain(effector_id, gain)

    def getScale(self, effector_id):
        return self.joints_list[effector_id].scale

    def set_angle_gain(self, effector_id, scale):
        self.joints_list[effector_id].scale = scale

    def initialise_effectors(self):
        for effector in EffectorJoints:
            self.joints_list[effector] = NaoJoint(
                effector_to_range[effector][0], effector_to_range[effector][1],
                2.0)

    def get_accel_rates(self):
        return self.accel_rates

    def set_accel_rates(self, accel_rates):
        self.accel_rates = accel_rates

    def set_gyro_rates(self, rates):
        self.prev_gyro_rates = self.gyro_rates
        self.gyro_rates = rates

    def get_gyro_rates(self):
        return self.gyro_rates

    def reached_target(self, effector_id):
        effector = self.joints_list[effector_id]
        angle = effector.target_angle
        current_angle = effector.current_angle
        return abs(angle - current_angle) < effector.error_tolerance

    def compute_torque(self, effector_id):

        effector = self.joints_list[effector_id]
        gain = effector.scale
        angle = effector.target_angle

        current_angle = effector.current_angle

        if angle >= effector.max_angle:
            angle = effector.max_angle

        elif angle <= effector.min_angle:
            angle = effector.min_angle

        if abs(angle - current_angle) < effector.error_tolerance:
            return 0
        elif current_angle < angle:
            return math.radians(abs(angle - current_angle)) * gain
        elif current_angle > angle:
            return -math.radians(abs(angle - current_angle)) * gain