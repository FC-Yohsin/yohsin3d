from behavior import DrawingBehavior
from yohsin3d import Agent, AgentLocation

coords = AgentLocation((-14.4, 0.0), 0)
behavior = DrawingBehavior(start_coordinates=coords)

agent = Agent(agent_num=2,
              global_port=3100,
              host_name="localhost",
              team_name="MyTeam",
              behavior=behavior,
              )


behavior.initialize_behavior()

agent.start()
