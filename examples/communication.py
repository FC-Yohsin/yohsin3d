import sys

from yohsin3d import Agent, BaseBehavior
from yohsin3d.localizers import GroundTruthLocalizer
from yohsin3d.core import Yohsin3dCommunicator, CommunicationData, AgentLocation


class DerivedBehavior(BaseBehavior):
    def __init__(self, start_coordinates: AgentLocation=None, localizer=None, communicator=None) -> None:
        super().__init__(beam_location=start_coordinates, localizer=localizer, communicator=communicator)

    def hear(self) -> CommunicationData:
        data = self.communicator.hear()
        return data

    def act(self):
        x = self.hear()
        print("HEAR", x.ball_x)


num = int(sys.argv[1])
coords =  AgentLocation((-14.4, 0.0), 0) if num == 1 else AgentLocation((-12.4, 0.0), 180)
localizer = GroundTruthLocalizer()
communicator = Yohsin3dCommunicator()
behavior = DerivedBehavior(start_coordinates=coords, localizer=localizer, communicator=communicator)

agent = Agent(agent_num=sys.argv[1],
              global_port=3100,
              host_name="localhost",
              team_name="MyTeam",
              behavior=behavior,
              )

agent.start()
