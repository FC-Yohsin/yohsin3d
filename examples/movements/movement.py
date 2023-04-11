from yohsin3d import Agent, AgentLocation, BaseBehavior
from yohsin3d.movement import Movement, MovementPhase
from yohsin3d.core.common import Joint


def create_wave_skill():
    def move_arm_phase1():
        phase = MovementPhase(0.5)
        phase.add(Joint.RA1, -120, 15.0)
        phase.add(Joint.RA2, -95, 15.0)
        phase.add(Joint.RA3, -120, 15.0)
        phase.add(Joint.RA4, 0, 15.0)
        return phase
    
    def move_arm_phase2():
        phase = MovementPhase(0.5)
        phase.add(Joint.RA1, -120, 15.0)
        phase.add(Joint.RA2, -95, 15.0)
        phase.add(Joint.RA3, -120, 15.0)
        phase.add(Joint.RA4, 90, 15.0)
        return phase

    def get_phases():
        return [move_arm_phase1(), move_arm_phase2()]
    
    wave_skill = Movement()
    wave_skill.add_phases(get_phases())
    return wave_skill


wave_skill = create_wave_skill()

class MovementBehavior(BaseBehavior):
    def __init__(self, start_coordinates: AgentLocation=None, communicator=None, localizer=None) -> None:
        super().__init__(beam_location=start_coordinates, communicator=communicator,  localizer=localizer)

    def act(self):
        wave_skill.perform(behavior.body_model, behavior.world_model)
        if wave_skill.is_finished():
            wave_skill.reset()
        

coords =  AgentLocation((-14.4, 0.0), 0)
behavior = MovementBehavior(start_coordinates=coords)

agent = Agent(agent_num=2,
              global_port=3100,
              host_name="localhost",
              team_name="MyTeam",
              behavior=behavior,
              )

agent.start()
