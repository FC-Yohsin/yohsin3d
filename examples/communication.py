import sys

from yohsin3d import Agent, BaseBehavior, AgentLocation
from yohsin3d.localizers import GroundTruthLocalizer
from yohsin3d.communicators import Y3dCommunicator


class DerivedBehavior(BaseBehavior):
    def __init__(self, start_coordinates: AgentLocation=None, localizer=None, communicator=None) -> None:
        super().__init__(beam_location=start_coordinates, localizer=localizer, communicator=communicator)
        self.communicator: Y3dCommunicator

    def act(self):
        data = self.communicator.heard_data
        print(data.ball_x)

        
num = int(sys.argv[1])
coords =  AgentLocation((-14.4, 0.0), 0) if num == 1 else AgentLocation((-12.4, 0.0), 180)
localizer = GroundTruthLocalizer()
communicator = Y3dCommunicator()
behavior = DerivedBehavior(start_coordinates=coords, localizer=localizer, communicator=communicator)

agent = Agent(agent_num=sys.argv[1],
              global_port=3100,
              host_name="localhost",
              team_name="MyTeam",
              behavior=behavior,
              )

agent.start()
