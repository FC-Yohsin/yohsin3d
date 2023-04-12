from yohsin3d import Spawner
from yohsin3d import Agent, AgentLocation, BaseBehavior

class DerivedBehavior(BaseBehavior):
    def __init__(self, start_coordinates: AgentLocation = None, communicator=None, localizer=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=communicator,  localizer=localizer)

    def act(self):
        pass


types = {
    1: 0,
    2: 0,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 4,
    10: 4,
    11: 4,
}

positions = {
    1 : (-14.4, 0.0), 
    2 :  (-11.0, 5.5), 
    3 : (-11.0, -5.5), 
    4 : (-0.65, 7.0), 
    5 : (-0.65, -7.0), 
    6 : (-7.5, -3.2),  
    7 : (-7.5, 3.2), 
    8 : (-5.8, 0.0), 
    9 : (-5, 7),  
    10 : (-5, -7), 
    11 : (-2.3, 0.0), 
}



team = Spawner()
for i in range(1, 12):
    coords = AgentLocation(positions[i], 0)
    behavior = DerivedBehavior(start_coordinates=coords)

    agent = Agent(agent_num=i,
                  agent_type=types[i],
                  global_port=3100,
                  host_name="localhost",
                  team_name="MyTeam",
                  behavior=behavior,
              )
    
    team.add(agent)

team.start()