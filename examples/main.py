from yohsin3d import Agent, BaseBehavior


class DerivedBehavior(BaseBehavior):
    def __init__(self, start_coordinates=(0,0)) -> None:
        super().__init__(start_coordinates=start_coordinates)

    def act(self):
        # Add the brain
        pass

behavior = DerivedBehavior(start_coordinates=(-14.4, 0.0))
agent = Agent(agent_num=1,
                global_port=3100,
                host_name="localhost",
                team_name="MyTeam",
                behavior=behavior
                )

agent.start()

