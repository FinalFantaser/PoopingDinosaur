from pygame.time import get_ticks

from objects import (
    Object,

    # ... NPC
    Dinosaur,
    TRexNew,
    Human,

    LandMine,
    Skyscraper,
    Missile,

    Explosion, Jeep,
)
from .object_handler import ObjectHandler
from data_containers import objects as obj_container

class ExplosionHandler(ObjectHandler):
    DESTRUCTIBLES: tuple[type[Object], ...] = (
        # ... NPC
        Dinosaur,
        TRexNew,
        Human,
        Jeep,

        LandMine,
        Skyscraper,
        Missile,
    )

    @classmethod
    def update(cls, obj: Explosion) -> None:
        curr_ticks = get_ticks()

        if obj.damage and obj.curr_frame == int(obj.TOTAL_FRAMES/2):
            for other_obj in obj_container.main_layer().values():
                if other_obj is obj:
                    continue

                if not isinstance(other_obj, cls.DESTRUCTIBLES):
                    continue

                if not getattr(other_obj, "hitbox", other_obj.rect).overlaps(obj.rect):
                    continue

                if isinstance(other_obj, TRexNew):
                    if other_obj.invincibility < 1:
                        other_obj.invincibility = other_obj.INVINCIBILITY_DURATION
                        other_obj.health -= 1
                        other_obj.vel_x = -other_obj.VEL_X_MIN
                        other_obj.vel_y = other_obj.JUMP_ACCEL
                elif isinstance(other_obj, Skyscraper):
                    other_obj.health -= 1
                elif isinstance(other_obj, LandMine):
                    other_obj.triggered_at = curr_ticks - other_obj.TRIGGER_DELAY
                else:
                    obj_container.queue_delete(other_obj)

        if obj.curr_frame >= obj.total_frames - 1 and curr_ticks - obj.last_frame_change >= obj.anim_interval:
            obj_container.queue_delete(obj)

            if obj.spawn is not None:
                obj_container.queue_add(obj.spawn)

        obj.last_update = curr_ticks