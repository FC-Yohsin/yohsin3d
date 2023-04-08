from yohsin3d import Agent, BaseBehavior, GroundTruthLocalizer


class DerivedBehavior(BaseBehavior):
    def __init__(self, start_coordinates=(0,0), localizer=None) -> None:
        super().__init__(start_coordinates=start_coordinates, localizer=localizer)

    def act(self):
        print(self.localizer.my_location.position)

localizer = GroundTruthLocalizer()
behavior = DerivedBehavior(start_coordinates=(-14.4, 0.0), localizer=localizer)

agent = Agent(agent_num=1,
                global_port=3100,
                host_name="localhost",
                team_name="MyTeam",
                behavior=behavior,
                )

agent.start()

