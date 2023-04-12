from yohsin3d import Spawner, Agent, AgentLocation
from behavior import Y3dCommunicatorBehavior
from team_info import types, positions

agent_spawner = Spawner()

for i in range(1, 3):
    coords = AgentLocation(positions[i], 0)
    behavior = Y3dCommunicatorBehavior(start_coordinates=coords)

    agent = Agent(agent_num=i,
                  agent_type=types[i],
                  global_port=3100,
                  host_name="localhost",
                  team_name="MyTeam",
                  behavior=behavior,
              )
    
    agent_spawner.add(agent)

agent_spawner.start()