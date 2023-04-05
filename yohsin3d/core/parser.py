import re
from typing import List
from .body.body_model import *
from .world.world_model import *

class Parser:

    def __init__(self,
                 world_model=None,
                 body_model=None,
                 team_name="test") -> None:

        self.world_model: WorldModel = world_model
        self.body_model: BodyModel = body_model
        self.side = SIDE_LEFT
        self.team_name = team_name

    def parse(self, message: str):
        return True