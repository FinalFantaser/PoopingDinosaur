from pygame.time import get_ticks

import core.video
from objects import Rect, Layer, Direction, Object, Ground, Camera, Skyscraper, Explosion
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class SkyscraperHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Skyscraper):
        time_delta = obj.update_delta

        obj.invincibility = max(0, obj.invincibility - time_delta)
        dest_angle: float = Skyscraper.MAX_ANGLE + (abs(Skyscraper.MAX_ANGLE) / obj.max_health * obj.health)

        if obj.angle > dest_angle:
            obj.rotate(time_delta * obj.DEGREES_PER_MS)
        elif obj.angle <= obj.MAX_ANGLE:
            num_of_explosions = int(obj.texture_rotated.get_width() / Explosion.WIDTH)
            pos_x = obj.x
            pos_y = obj.rect.bottom - Explosion.HEIGHT/2

            for _ in range(num_of_explosions):
                new_explosion = Explosion((pos_x, pos_y))
                obj_container.queue_delete(obj)
                obj_container.queue_add(new_explosion)
                pos_x += Explosion.WIDTH

        obj.last_update = get_ticks()