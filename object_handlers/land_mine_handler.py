from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, LandMine, Explosion
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class LandMineHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: LandMine):
        if cls.delete_if_passed_camera(obj):
            return

        curr_ticks = get_ticks()

        if obj.triggered_at is not None:
            if curr_ticks - obj.triggered_at >= obj.TRIGGER_DELAY:
                # Create explosions
                x = obj.trigger_area.x
                y = obj_container.get_ground().touch_level - Explosion.HEIGHT/2
                for _ in range(int(obj.trigger_area.width/Explosion.WIDTH)):
                    obj_container.queue_add(
                        Explosion(pos=(x,y), damage=True)
                    )
                    x += Explosion.WIDTH

                obj_container.queue_delete(obj)
                return
        else:
            for dinosaur in obj_container.dinosaurs().values():
                if dinosaur.hitbox.overlaps(obj.trigger_area) and dinosaur.invincibility < 1:
                    obj.triggered_at = curr_ticks
                    break

        obj.last_update = curr_ticks
