from yohsin3d import AgentType

BEFORE_KICKOFF_FORMATION = {
    1 : (-14.4, 0.0), # Goalie
    2 :  (-11.0, 5.5), # Defender left
    3 : (-11.0, -5.5), # Defender right
    4 : (-0.65, 7.0), # Midfielder left
    5 : (-0.65, -7.0), # Midfielder right
    6 : (-7.5, -3.2),  # Forward left
    7 : (-7.5, 3.2), # Forward right
    8 : (-5.8, 0.0), # Striker
    9 : (-5, 7),  # Supporter left
    10 : (-5, -7), # Supporter right
    11 : (-2.3, 0.0), # Supporter center
}




# During the game place the robot uniformly in the field
# Field size is 30x20
PLAYON_POSITIONS = {
    1 : (-14.4, 0.0), 
    2 :  (-12.0, 2.5),  
    3 : (-12.0, -2.5), 
    4 : (-8, 7), 
    5 : (-8, -7), 
    6 : (0, 4),  
    7 : (0, -4),
    8 : (2, 0.0), 
    9 : (10, 6), 
    10 : (10,-6), 
    11 : (12.5, 0),  
}


TYPES = {
    1: AgentType.NAO,
    2: AgentType.NAO,
    3: AgentType.NAO_HETERO_1,
    4: AgentType.NAO_HETERO_1,
    5: AgentType.NAO_HETERO_2,
    6: AgentType.NAO_HETERO_2,
    7: AgentType.NAO_HETERO_3,
    8: AgentType.NAO_HETERO_3,
    9: AgentType.NAO_HETERO_4,
    10: AgentType.NAO_HETERO_4,
    11: AgentType.NAO,
}