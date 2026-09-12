from pygame.time import get_ticks
from objects import Object, Obstacle, TRexNew, Allosaurus, FlattenedObject
from .object_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler
from data_containers import objects as obj_container, game_data


class AllosaurusHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Allosaurus) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        update_delta = obj.last_update

        # Accelerate
        # accel_x = obj.VEL_X_MAX / obj.VEL_X_MAX_IN / 1000 * update_delta * obj.direction.value[0]
        # obj.vel_x = min(
        #     obj.vel_x + (accel_x if obj.hitbox.bottom >= obj_container.get_ground().touch_level else 0),
        #     obj.VEL_X_MAX
        # )

        obj.last_update = get_ticks()