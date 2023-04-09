from yohsin3d import Agent, AgentLocation, BaseBehavior, BaseCommunicator


class DerivedBehavior(BaseBehavior):
    def __init__(self, start_coordinates: AgentLocation = None, communicator=None, localizer=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=communicator,  localizer=localizer)

    def act(self):
        pass


coords = AgentLocation((-14.4, 0.0), 0)
behavior = DerivedBehavior(start_coordinates=coords)

agent = Agent(agent_num=2,
              global_port=3100,
              host_name="localhost",
              team_name="MyTeam",
              behavior=behavior,
              )

agent.start()
