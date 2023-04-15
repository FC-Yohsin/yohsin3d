from behavior import GetUpBehavior
from yohsin3d import Agent, AgentLocation
from yohsin3d.localizers import GroundTruthLocalizer

coords = AgentLocation((-14.4, 0.0), 0)
behavior = GetUpBehavior(start_coordinates=coords, localizer=GroundTruthLocalizer())

agent = Agent(agent_num=2,
              global_port=3100,
              host_name="localhost",
              team_name="MyTeam",
              behavior=behavior,
              )
behavior.initialize_behavior()
agent.start()
