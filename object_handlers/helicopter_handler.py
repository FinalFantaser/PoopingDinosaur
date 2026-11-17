from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Helicopter, TRexNew
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class HelicopterHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Helicopter):
        time_delta = obj.update_delta

        # Your code here ...
        # ...

        obj.last_update = get_ticks()

    @classmethod
    def track_target(cls, helicopter: Helicopter, time_delta: int) -> None:
        trex = obj_container.get(TRexNew.ID, True)

        if helicopter.rect.center_x < trex.rect.center_x - helicopter.TARGET_TRACKING_MIN:
            helicopter.engine_power_x += helicopter.ENGINE_POWER_X * time_delta

    @classmethod
    def maintain_altitude(cls, helicopter: Helicopter, time_delta: int) -> None:
        if helicopter.y < helicopter.ALTITUDE_MIN:
            helicopter.vel_y -= helicopter.ENGINE_POWER_Y * time_delta
