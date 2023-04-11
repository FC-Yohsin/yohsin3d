import sys

from yohsin3d import Agent, BaseBehavior, AgentLocation, BaseCommunicator

class CustomCommunicator(BaseCommunicator):
    def __init__(self) -> None:
        super().__init__()
        self.heard_data: str = None

    def say(self) -> None:
        self.said_message = f"Hello{self.world_model.my_number}"

    def hear(self) -> str:
        heard_message = self.heard_message
        message = heard_message.message
        self.heard_data = message


class CommunicatingBehavior(BaseBehavior):
    def __init__(self, start_coordinates: AgentLocation = None, localizer=None, communicator=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         localizer=localizer, communicator=communicator)
        self.communicator: CustomCommunicator

    def act(self):
        data = self.communicator.heard_data
        print(data)


num = int(sys.argv[1])
coords = AgentLocation(
    (-14.4, 0.0), 0) if num == 1 else AgentLocation((-12.4, 0.0), 180)
communicator = CustomCommunicator()
behavior = CommunicatingBehavior(start_coordinates=coords, communicator=communicator)

agent = Agent(agent_num=sys.argv[1],
              global_port=3100,
              host_name="localhost",
              team_name="MyTeam",
              behavior=behavior,
              )

agent.start()
