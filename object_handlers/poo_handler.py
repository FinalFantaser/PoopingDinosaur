import pygame.time
from objects import Poo, Ground
from object_handlers.object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class PooHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Poo) -> None:
        update_delta: int = obj.update_delta

        if not obj_container.get_camera().within_viewpoint(obj):
            obj_container.queue_delete(obj)
            return

        ground: Ground = obj_container.get_ground()

        # Gravity
        if obj.rect.bottom < ground.touch_level:
            fall_accel: float = game_data.GRAVITY_PIXELS * obj.weight_factor
            obj.vel_y += fall_accel/1000 * update_delta
        else:
            obj.vel_y = 0


        accel_y: float = obj.vel_y / 1000 * obj.update_delta
        obj.rect.bottom = min(obj.rect.bottom + accel_y, ground.touch_level)

        obj.last_update = pygame.time.get_ticks()
