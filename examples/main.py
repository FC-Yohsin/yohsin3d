from yohsin3d import Agent, BaseBehavior
from yohsin3d.localizers import GroundTruthLocalizer
from yohsin3d.core import AgentLocation



class DerivedBehavior(BaseBehavior):
    def __init__(self, start_coordinates: AgentLocation=None, localizer=None) -> None:
        super().__init__(beam_location=start_coordinates, localizer=localizer)

    def act(self):
        pass
        

coords =  AgentLocation((-14.4, 0.0), 0)
localizer = GroundTruthLocalizer()
behavior = DerivedBehavior(start_coordinates=coords, localizer=localizer)

agent = Agent(agent_num=2,
              global_port=3100,
              host_name="localhost",
              team_name="MyTeam",
              behavior=behavior,
              )

agent.start()
