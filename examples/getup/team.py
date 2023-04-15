
from behavior import GetUpBehavior
from yohsin3d import Agent, AgentType, Spawner, AgentLocation

types = {
    1: AgentType.NAO,
    2: AgentType.NAO_HETERO_1,
    3: AgentType.NAO_HETERO_2,
    4: AgentType.NAO_HETERO_3,
    5: AgentType.NAO_HETERO_4,
}

positions = {
    1: (-12.4, -3.0),
    2: (-12.4, -1.0),
    3: (-12.4, 1.0),
    4: (-12.4, 3.0),
    5: (-12.4, 5.0),
}


agent_spawner = Spawner()

for i in range(1, 6):
    coords = AgentLocation(positions[i], 0)
    behavior = GetUpBehavior(start_coordinates=coords)

    agent = Agent(agent_num=i,
                  agent_type=types[i],
                  global_port=3100,
                  host_name="localhost",
                  team_name="MyTeam",
                  behavior=behavior,
                  )
    behavior.initialize_behavior()

    agent_spawner.add(agent)

agent_spawner.start()
