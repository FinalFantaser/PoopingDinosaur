from data_containers import objects as obj_container, game_data
from objects import *


class ObjectHandler:
    @classmethod
    def update(cls, obj: Object) -> None:
        pass

    @classmethod
    def read_input(cls, obj: Object) -> None:
        pass

    @classmethod
    def delete_if_passed_camera(cls, obj: Object) -> bool:
        camera: Camera = obj_container.get_camera()

        if obj.rect.right < camera.rect.left or obj.rect.right > camera.rect.right + obj.width * 3:
            obj_container.queue_delete(obj)
            return True

        return False

    @classmethod
    def physics(cls, obj: Object) -> None:
        for att in 'vel_x', 'vel_y', 'WEIGHT_FACTOR':
            if not hasattr(obj, att):
                return

        cls.gravity(obj)

        # Horizontal movement
        obj.x += (obj.vel_x / 1000 * obj.update_delta) * obj.direction.value[0]

    @classmethod
    def gravity(cls, obj: Object) -> None:
        update_delta: int = obj.update_delta
        ground: Ground = obj_container.get_ground()

        if obj.rect.bottom < ground.touch_level:
            fall_accel: float = game_data.GRAVITY_PIXELS * obj.WEIGHT_FACTOR
            obj.vel_y += fall_accel / 1000 * update_delta

        obj.y += obj.vel_y / 1000 * update_delta
        if obj.rect.bottom >= ground.touch_level:
            obj.vel_y = 0.0
            obj.rect.bottom = ground.touch_level