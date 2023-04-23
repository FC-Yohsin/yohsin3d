FIELD_Y = 20
FIELD_X = 30
HALF_FIELD_Y = FIELD_Y / 2.0
HALF_FIELD_X = FIELD_X / 2.0

min_ball_x = -HALF_FIELD_X - 2.0
max_ball_x = HALF_FIELD_X + 2.0
min_ball_y = -HALF_FIELD_Y - 2.0
max_ball_y = HALF_FIELD_Y + 2.0

min_agent_x = -HALF_FIELD_X - 5.0
max_agent_x = HALF_FIELD_X + 5.0
min_agent_y = -HALF_FIELD_Y - 5.0
max_agent_y = HALF_FIELD_Y + 5.0

NUM_AGENTS = 11


WORLD_OBJECTS_GLOBAL_POSITIONS = {
    "F1R": (15.0, 10.0, 0.0),
    "F1L": (-15.0, 10.0, 0.0),
    "F2R": (15.0, -10.0, 0.0),
    "F2L": (-15.0, -10.0, 0.0),
    "G1L": (-15.0, 1.05, 0.8),
    "G2L": (-15.0, -1.05, 0.8),
    "G1R": (15.0, 1.05, 0.8),
    "G2R": (15.0, -1.05, 0.8),
}

GOAL_MID_POSITION = (15.0, 0.0)
