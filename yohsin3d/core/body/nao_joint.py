from typing import Tuple

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
        self.k1, self.k2, self.k3 = (0,0,0)
        self.reset_errors()

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


    def reset_errors(self):
        self.current_error = 0
        self.previous_error = 0
        self.cumulative_error = 0

    def update_errors(self):
        self.previous_error = self.current_error
        self.current_error = self.target_angle - self.current_angle
        self.cumulative_error += self.current_error