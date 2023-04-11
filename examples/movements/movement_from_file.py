from yohsin3d import Agent, AgentLocation, BaseBehavior
from yohsin3d.movement import Movement

wave_skill = Movement.from_file('examples/movements/data/wave.txt')

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
