from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, LandMine
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class LandMineHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: LandMine):
        time_delta = obj.update_delta

        if cls.delete_if_passed_camera(obj):
            return

        curr_ticks = get_ticks()

        if obj.triggered_at is not None:
            if curr_ticks - obj.triggered_at >= obj.TRIGGER_DELAY:
                # Create explosions...
                obj_container.queue_delete(obj)
                return
        else:
            for dinosaur in obj_container.dinosaurs().values():
                if dinosaur.hitbox.overlaps(obj.trigger_area):
                    obj.triggered_at = curr_ticks
                    break
        
        obj.last_update = curr_ticks

