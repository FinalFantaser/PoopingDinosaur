from telnetlib import Telnet

from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Tesla, Lighting
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class TeslaHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Tesla):
        # Teslas are handled in couples only
        if obj.left is None:
            return

        if cls.delete_if_passed_camera(obj):
            return

        time_delta = obj.update_delta

        # Wrappers for general convenience
        left_tesla: Tesla = obj_container.get(obj.left)
        right_tesla: Tesla = obj

        # Charge
        charge_growth = Tesla.CHARGE_MAX / right_tesla.charge_interval * time_delta
        left_tesla.charge = right_tesla.charge = min(right_tesla.charge + charge_growth, Tesla.CHARGE_MAX)

        # Discharge
        if right_tesla.charge >= Tesla.CHARGE_MAX:
            left_tesla.charge = right_tesla.charge = 0
            left_tesla.curr_frame = right_tesla.curr_frame = 0

            start_x = left_tesla.rect.right
            for _ in range(left_tesla.gap):
                new_lighting = Lighting((start_x, left_tesla.y))
                obj_container.queue_add(new_lighting)
                start_x += Lighting.WIDTH

        left_tesla.last_update = right_tesla.last_update = get_ticks()

    @classmethod
    def delete_if_passed_camera(cls, obj: Tesla) -> bool:
        # Teslas are always coupled, hence they are deleted in couples only
        camera = obj_container.get_camera()
        if camera.left - obj.rect.right >= camera.width:
            obj_container.queue_delete(obj_container.get(obj.left))
            obj_container.queue_delete(obj)
            return True

        return False