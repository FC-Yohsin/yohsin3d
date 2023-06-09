from yohsin3d import Spawner, Agent, AgentLocation
from soccer_behavior import SoccerBehavior
from team_info import types, positions

agent_spawner = Spawner()

for i in range(1, 12):
    coords = AgentLocation(positions[i], 0)
    behavior = SoccerBehavior(start_coordinates=coords)

    agent = Agent(agent_num=i,
                  agent_type=types[i],
                  global_port=3100,
                  host_name="localhost",
                  team_name="MyTeam",
                  behavior=behavior,
                  )

    agent_spawner.add(agent)

agent_spawner.start()
