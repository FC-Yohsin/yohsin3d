from yohsin3d import Agent, BaseBehavior, EffectorJoints, PlayModes
import math
from typing import Dict



def getPFSWalk(counter, diff, radians_to_move):

    T = 0.32
    t = counter / 50


    laj1 = -2.0
    raj1 = -2.0
    laj2 = 0.35
    raj2 = -0.35

			
    laj3 = -1.4
    raj3 = 1.4
    laj4 = -0.52
    raj4 = 0.52
        
    # Hip Yaw Pitch
    llj1 = -0.03    
    rlj1 = -0.03

    # Hip Roll
    llj2 = 0.03
    rlj2 = -0.03
    
    # Hip Pitch
    llj3 = 0.382 + 0.75 * \
        math.sin(2 * math.pi * t / T - math.pi / 2 + 1.165)
    rlj3 = 0.382 + 0.72 * \
        math.sin(2 * math.pi * t / T + math.pi / 2 + 1.165)

    # Knee Pitch
    llj4 = -0.61 + 0.425 * \
        math.sin(2 * math.pi * t / T - math.pi / 2 - 1.115)
    rlj4 = -0.61 + 0.425 * \
        math.sin(2 * math.pi * t / T + math.pi / 2 - 1.115)

    # Foot Pitch
    llj5 = 0.465 + 0.425 * \
        math.sin(2 * math.pi * t / T + math.pi / 2 - 0.325)
    rlj5 = 0.465 + 0.425 * \
        math.sin(2 * math.pi * t / T - math.pi / 2 - 0.325)

    # Foot Roll
    llj6 = -0.03
    rlj6 = 0.03

    move_llj2 = 0.03 + 0.03 * math.sin(2 * math.pi * t / T - math.pi / 2 - 0.3)
    move_rlj2 = -0.03 + 0.03 * math.sin(2 * math.pi * t / T + math.pi / 2 - 0.3)
    move_llj6 = -0.03 + 0.03 * math.sin(2 * math.pi * t / T + math.pi / 2 - 0.3)
    move_rlj6 = 0.03 + 0.03 * math.sin(2 * math.pi * t / T - math.pi / 2 - 0.3)


    if (diff < 0.13 or diff > 6.15):
        llj2 = move_llj2
        rlj2 = move_rlj2

        llj6 = move_llj6
        rlj6 = move_rlj6
    

    elif (radians_to_move < 0):     
        llj2 = move_llj2 - 0.01
        rlj2 = move_rlj2 - 0.01

        llj6 = move_llj6 - 0.01
        rlj6 = move_rlj6 - 0.01
    
    elif (radians_to_move > 0):     
        llj2 = move_llj2 + 0.01    
        rlj2 = move_rlj2 + 0.01

        llj6 = move_llj6 + 0.01 
        rlj6 = move_rlj6 + 0.01


    return {
        EffectorJoints.EFF_LA1: laj1,
        EffectorJoints.EFF_LA2: laj2,
        EffectorJoints.EFF_LA3: laj3,
        EffectorJoints.EFF_LA4: laj4,
        EffectorJoints.EFF_RA1: raj1,
        EffectorJoints.EFF_RA2: raj2,
        EffectorJoints.EFF_RA3: raj3,
        EffectorJoints.EFF_RA4: raj4,
        
        EffectorJoints.EFF_LL1: llj1,
        EffectorJoints.EFF_LL2: llj2,
        EffectorJoints.EFF_LL3: llj3,
        EffectorJoints.EFF_LL4: llj4,
        EffectorJoints.EFF_LL5: llj5,
        EffectorJoints.EFF_LL6: llj6,
        EffectorJoints.EFF_RL1: rlj1,
        EffectorJoints.EFF_RL2: rlj2,
        EffectorJoints.EFF_RL3: rlj3,
        EffectorJoints.EFF_RL4: rlj4,
        EffectorJoints.EFF_RL5: rlj5,
        EffectorJoints.EFF_RL6: rlj6
    }
    



def get_angle(point_1, point_2):
    angle = math.atan2(point_1[1] - point_2[1], point_1[0] - point_2[0])
    angle = math.degrees(angle)
    return angle

class DerivedBehavior(BaseBehavior):
    def __init__(self, start_coordinates=(0,0)) -> None:
        super().__init__(start_coordinates=start_coordinates)
        self.counter = 0
        self.gain = 4

    def set_targets(self, joint_to_angle_map: Dict[EffectorJoints, float]):
        for joint, angle in joint_to_angle_map.items():
            angle = math.degrees(angle)
            self.body_model.set_target_angle(joint, angle, self.gain)

    def act(self):
        if self.world_model.playmode == PlayModes.PM_PLAY_ON:
            self.counter += 1

            current_orientation = math.radians(self.world_model.orientation_groundtruth)
            target = (0,0)
            agent_pos = self.world_model.position_groundtruth[:2]
            desired_orientation = get_angle(target, agent_pos)
            desired_orientation = math.radians(desired_orientation)
            orientation_to_move = desired_orientation - current_orientation

            if (orientation_to_move < -math.pi):
                orientation_to_move = orientation_to_move + (2 * math.pi)
            if desired_orientation < 0:
                desired_orientation = math.pi + (math.pi + desired_orientation)

            if self.gain <= 10:
                self.gain += 0.05

            joints = getPFSWalk(self.counter, abs(current_orientation - desired_orientation), orientation_to_move)
            self.set_targets(joints)
    
        

behavior = DerivedBehavior(start_coordinates=(-14.4, 0.0))
agent = Agent(agent_num=1,
                global_port=3100,
                host_name="localhost",
                team_name="FCYohsin",
                behavior=behavior
                )

agent.start()

