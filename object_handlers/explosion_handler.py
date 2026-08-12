from pygame.time import get_ticks

from objects import Explosion
from .object_handler import ObjectHandler
from data_containers import objects as obj_container

class ExplosionHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Explosion) -> None:
        if obj.curr_frame >= obj.TOTAL_FRAMES - 1 and get_ticks() - obj.last_frame_change >= obj.anim_interval:
            obj_container.queue_delete(obj)

            if obj.spawn is not None:
                obj_container.queue_add(obj.spawn)

            return

        obj.last_update = get_ticks()