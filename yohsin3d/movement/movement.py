from typing import List
import re

from ..core.common import Joint, joint_to_effector, effector_to_joint
from ..core.body import BodyModel
from ..core.world import WorldModel


class MovementJoint:
    def __init__(self, joint: Joint, angle: float, speed: float):
        self.joint = joint
        self.angle = angle
        self.speed = speed

    def move(self, agent: BodyModel):
        agent.set_target_angle(self.joint, self.angle, self.speed)


class MovementPhase:
    def __init__(self, wait_time) -> None:
        self.movement_joints: List[MovementJoint] = []
        self.wait_time = wait_time
        self.has_started = False
        self.start_time = 0.0

    def set_start_time(self, time: float):
        self.start_time = time

    def add(
        self,
        effector: Joint,
        angle,
        speed=1.0,
    ) -> None:
        movement_joint = MovementJoint(effector, angle, speed)
        self.movement_joints.append(movement_joint)

    def perform(self, agent: BodyModel) -> None:
        for movement_joint in self.movement_joints:
            movement_joint.move(agent)

    def reset(self):
        self.has_started = False


class Movement:
    def __init__(self, name="None") -> None:
        self.name = name
        self.phases: List[MovementPhase] = []
        self.current_index = 0

    @staticmethod
    def from_string(content: str):
        movement = Movement()
        phases: list = list(re.findall(
            r"start phase((.|\n)*?)end phase", content))

        for phase in phases:
            phase_details: str = phase[0]
            lines = phase_details.splitlines()
            first_line = lines[0].strip()
            wait_time = float(first_line.split(":")[1])
            movement_phase = MovementPhase(wait_time)
            lines = lines[1:]
            for line in lines:
                line = line.strip()
                if line == "":
                    continue
                line = line.split(" ")
                if line[0] == "target":
                    joint = line[1]
                    joint = (effector_to_joint[joint])
                    angle = float(line[2])
                    speed = float(line[3])
                    movement_phase.add(joint, angle, speed)
                else:
                    raise Exception("Invalid file")

            movement.add(movement_phase)

        return movement

    @staticmethod
    def from_file(path):
        file = open(path, 'r')
        content = file.read()
        movement = Movement.from_string(content)
        file.close()
        return movement

    def is_finished(self):
        finished = self.current_index >= len(self.phases)
        return finished

    def add_phases(self, phases: List[MovementPhase]):
        for phase in phases:
            self.add(phase)

    def add(self, phase):
        self.phases.append(phase)

    def perform(self, agent: BodyModel, world: WorldModel) -> None:

        if self.is_finished():
            return

        current_time = world.get_time()
        current_phase = self.phases[self.current_index]

        if not current_phase.has_started:
            current_phase.perform(agent)
            current_phase.set_start_time(current_time)
            current_phase.has_started = True

        elapsed_time = current_time - current_phase.start_time

        if elapsed_time >= current_phase.wait_time:
            self.current_index += 1

    def display(self):
        for phase in self.phases:
            print(f'Phase: {phase.wait_time}')
            for movement_joint in phase.movement_joints:
                print(
                    f'    {movement_joint.joint}: {movement_joint.angle} {movement_joint.speed}')

            print()

    def reset(self):
        self.current_index = 0
        for phase in self.phases:
            phase.reset()

    def write_to_file(self, path):
        file = open(path, 'w')

        state = 0
        for phase in self.phases:
            time = phase.wait_time
            data = f"start phase {state}: {time} "
            file.write(data)
            file.write('\n')
            for joint in phase.movement_joints:
                name = joint.joint
                name = joint_to_effector[name]
                angle = joint.angle
                speed = joint.speed
                data = f"target {name} {angle} {speed} "

                file.write(data)
                file.write('\n')

            file.write("end phase")
            file.write('\n')
            file.write('\n')

            state += 1

        file.close()
