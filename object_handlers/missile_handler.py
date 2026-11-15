import math
from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Missile
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class MissileHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Missile):
        time_delta = obj.update_delta

        # Your code here ...
        # ...

        obj.last_update = get_ticks()

    @classmethod
    def track_target(missile: Missile) -> None:
        if missile.target is None:
            # TODO Find target ...
            pass

        if missile.target is None:
            return

        target = obj_container.get(missile.target, False)
        if target is None:
            missile.target = None
            return

        delta_x = target.x - missile.x
        delta_y = target.y - missile.y
        target_angle = math.degrees(math.atan2(delta_x, delta_y))

        diff = (target_angle - missile.angle + 180) % 360 - 180

        max_turn = missile.ROTATION_SPEED / 1000 * missile.update_delta
        turn = max(-max_turn, min(diff, max_turn))

        missile.angle += turn

    @classmethod
    def physics(cls, obj: Missile) -> None:
        rad = math.radians(obj.angle)

        obj.vel_x = obj.SPEED * math.cos(rad)
        obj.vel_y = obj.SPEED * math.sin(rad)
