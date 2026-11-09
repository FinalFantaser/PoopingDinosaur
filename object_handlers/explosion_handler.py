from pygame.time import get_ticks

from objects import (
    Object,

    # ... NPC
    Dinosaur,
    TRexNew,
    TRexNewCave,

    LandMine,
    Skyscraper,
    # ... Missile

    Explosion,
)
from .object_handler import ObjectHandler
from data_containers import objects as obj_container

class ExplosionHandler(ObjectHandler):
    DESTRUCTIBLES: tuple[type[Object], ...] = (
        # ... NPC
        Dinosaur,
        TRexNew,
        TRexNewCave,

        LandMine,
        Skyscraper,
        # ... Missile
    )

    @classmethod
    def update(cls, obj: Explosion) -> None:
        if obj.damage and obj.curr_frame == int(obj.TOTAL_FRAMES/2):
                for other_obj in obj_container.main_layer().values():
                    if other_obj is obj:
                        continue

                    if not isinstance(other_obj, cls.DESTRUCTIBLES):
                        continue

                    if not getattr(other_obj, "hitbox", other_obj.rect).overlaps(obj.rect):
                        continue

                    if isinstance(other_obj, TRexNew|TRexNewCave):
                        if other_obj.invincibility < 1:
                            other_obj.invincibility = other_obj.INVINCIBILITY_DURATION
                            other_obj.health -= 1
                            other_obj.vel_x = -other_obj.VEL_X_MIN
                            other_obj.vel_y = other_obj.JUMP_ACCEL
                    elif isinstance(other_obj, Skyscraper):
                        other_obj.health -= 1
                    elif isinstance(other_obj, LandMine):
                        other_obj.triggered_at = get_ticks() - LandMine.TRIGGER_DELAY
                    else:
                        obj_container.queue_delete(other_obj)

        if obj.curr_frame >= obj.TOTAL_FRAMES - 1 and get_ticks() - obj.last_frame_change >= obj.anim_interval:
            obj_container.queue_delete(obj)

            if obj.spawn is not None:
                obj_container.queue_add(obj.spawn)

            return

        obj.last_update = get_ticks()