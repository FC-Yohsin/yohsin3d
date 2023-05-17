import math
from examples.strategy.constants import BEFORE_KICKOFF_FORMATION, PLAYON_POSITIONS, TYPES
from yohsin3d.core.world.enums import PlayModes
from yohsin3d.localizers import GroundTruthLocalizer
from yohsin3d.communicators import Y3dCommunicator, CommunicationData
from yohsin3d import Agent, AgentLocation, Spawner, BaseBehavior
from yohsin3d.locomotors import PFSWalk, PFSTurn


class SoccerBehavior(BaseBehavior):
    def __init__(self, start_coordinates=None, communicator=None, localizer=None) -> None:
        super().__init__(beam_location=start_coordinates,
                         communicator=communicator, localizer=localizer)
        self.communicator: Y3dCommunicator
        self.player_positions = {i: None for i in range(1, 12)}

    def initialize_walk_engine(self):
        self.pfs_walk = PFSWalk(
            self.body_model, self.world_model, self.localizer)
        self.pfs_turn = PFSTurn(
            self.body_model, self.world_model, self.localizer)

    def process_hear(self):
        heard_data: CommunicationData = self.communicator.heard_data
        heard_from = heard_data.heard_from

        if heard_from != None:
            self.player_positions[heard_data.heard_from] = (
                heard_data.my_x, heard_data.my_y)

    def get_closest_player_to_ball(self):
        closest_player = None
        closest_distance = 1000

        for i in range(1, 12):
            player_position = self.player_positions[i]
            ball = self.localizer.ball_position[:2]
            if player_position != None:
                distance = math.dist(player_position, ball)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_player = i

        return closest_player

    def act(self):
        self.process_hear()
        closest_player_to_ball = self.get_closest_player_to_ball()

        if closest_player_to_ball != None:

            if self.world_model.playmode == PlayModes.PLAY_ON:
                if self.world_model.my_number == closest_player_to_ball:
                    self.pfs_walk.dribble_to_goal()
                else:
                    self.pfs_walk.walk_to(
                        PLAYON_POSITIONS[self.world_model.my_number])
            else:
                self.pfs_walk.walk_to(
                    BEFORE_KICKOFF_FORMATION[self.world_model.my_number])


agent_spawner = Spawner()

for i in range(1, 12):

    localizer = GroundTruthLocalizer()
    communicator = Y3dCommunicator()

    behavior = SoccerBehavior(
        start_coordinates=AgentLocation(BEFORE_KICKOFF_FORMATION[i], 0),
        communicator=communicator,
        localizer=localizer
    )

    agent = Agent(agent_num=i,
                  agent_type=TYPES[i],
                  global_port=3100,
                  host_name="localhost",
                  team_name="MyTeam",
                  behavior=behavior,
                  )

    behavior.initialize_walk_engine()
    agent_spawner.add(agent)


if __name__ == "__main__":
    agent_spawner.start()
