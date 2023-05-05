from ..core import BaseLocalizer, VisibleObjects
import math


class GeometricLocalizer(BaseLocalizer):
    def __init__(self):
        super().__init__()
        self.global_static_objects_right = [
            VisibleObjects.F1R,
            VisibleObjects.G1R,
            VisibleObjects.G2R,
            VisibleObjects.F2R]
        self.global_static_objects_left = [
            VisibleObjects.F1L,
            VisibleObjects.G1L,
            VisibleObjects.G2L,
            VisibleObjects.F2L]

    def _get_straight_distance(self, distance, height):
        return math.sqrt((distance**2) - (height**2))

    def _search_two_visible_objects(
            self) -> tuple[VisibleObjects, VisibleObjects]:
        visible_objects = [visible_object for visible_object in self.world_model.simple_vision_objects.keys(
        ) if self.world_model.simple_vision_objects[visible_object] and visible_object != VisibleObjects.BALL]
        if len(visible_objects) >= 2:
            return (visible_objects[0], visible_objects[1])
        else:
            return None

    def _two_flag_position_localize(self,
                                    objects: tuple[VisibleObjects,
                                                   VisibleObjects]) -> tuple[float,
                                                                             float,
                                                                             float]:

        x1, y1, z1 = objects[0].global_position
        x2, y2, z2 = objects[1].global_position

        d1 = self._get_straight_distance(
            self.world_model.simple_vision_objects[objects[0]][0], height=0.414)
        d2 = self._get_straight_distance(
            self.world_model.simple_vision_objects[objects[1]][0], height=0.414)
        d3 = math.dist((x1, y1, z1), (x2, y2, z2))

        try:
            angle = math.acos(((d1**2) + (d3**2) - (d2**2)) / (2 * d1 * d3))
        except BaseException:
            angle = math.acos(1.0)

        X = d1 * math.cos(angle)
        Y = d1 * math.sin(angle)

        if objects[0] in self.global_static_objects_right and objects[1] in self.global_static_objects_right:
            x3, y3 = (x1 - Y, y1 - X)
        elif objects[0] in self.global_static_objects_left and objects[1] in self.global_static_objects_left:
            x3, y3 = (x1 + Y, y1 - X)
        elif objects[0] in self.global_static_objects_left and objects[1] in self.global_static_objects_right:
            x3, y3 = (x1 + X + 1.5, y1 - Y + 3.5)
        else:
            x3, y3 = (x1 + Y, y1 - X)

        return (x3, y3, 0)

    def _one_flag_orientation_localize(self, object: VisibleObjects) -> float:
        vision_data = self.world_model.simple_vision_objects[object]
        globalPositionOfWorldObject = object.global_position[0:2]
        currentPosition = self.my_location.position[0:2]

        phi = vision_data[1]
        hyp = math.dist(currentPosition,
                        globalPositionOfWorldObject)
        is_above = currentPosition[1] < globalPositionOfWorldObject[1]
        is_left = currentPosition[0] > globalPositionOfWorldObject[0]

        if is_above == is_left:
            base_axis = 1
        else:
            base_axis = 0

        base = abs(
            (globalPositionOfWorldObject[base_axis]) - (currentPosition[base_axis]))
        angle = base / hyp
        if math.radians(angle) == 90.0:
            angle -= 0.01
        theta = math.degrees(math.acos(angle)) - phi
        adjustement = 0

        if not is_above and not is_left:
            adjustement = -90
        elif not is_above and is_left:
            adjustement = 180
        elif is_above and not is_left:
            adjustement = 0
        elif is_above and is_left:
            adjustement = 90

        theta += adjustement

        return theta

    def _localize(self,
                  visible_objects: tuple[VisibleObjects,
                                         VisibleObjects]):
        pos = self._two_flag_position_localize(visible_objects)
        rounded_pos = (round(pos[0], 2), round(pos[1], 2), round(pos[2], 2))
        self.my_location.update_position(rounded_pos)

        if self.my_location.position is not None:
            orientation = self._one_flag_orientation_localize(
                visible_objects[0])
            rounded_orientation = round(orientation, 2)
            self.my_location.update_orientation(rounded_orientation)

    def update(self) -> None:
        visible_objects = self._search_two_visible_objects()
        if visible_objects is not None:
            self._localize(visible_objects)
