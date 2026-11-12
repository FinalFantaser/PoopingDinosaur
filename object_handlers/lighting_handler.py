from pygame.time import get_ticks
from objects import (
    Explosion,
    Lighting,
    TRexNew,
    TRexNewCave,
    Dinosaur,
    Human,
    # Missile
    LandMine,
)
from .object_handler import ObjectHandler
from data_containers import objects as obj_container


class LightingHandler(ObjectHandler):
    DESTRUCTIBLES: tuple[type[
        TRexNew
        |TRexNewCave
        |Dinosaur
        |Human
        |LandMine
    ]] = (
        TRexNew,
        TRexNewCave,
        Dinosaur,
        Human,
        # Missile
        LandMine,
    )

    @classmethod
    def update(cls, obj: Lighting):
        curr_ticks = get_ticks()

        if curr_ticks - obj.started_at >= Lighting.LIFESPAN:
            obj_container.queue_delete(obj)
            return

        for destructible in obj_container.main_layer().values():
            if destructible is obj:
                continue

            if not isinstance(destructible, cls.DESTRUCTIBLES):
                continue

            destructible_hitbox = getattr(destructible, 'hitbox', destructible.rect)
            if not obj.rect.overlaps(destructible_hitbox):
                continue

            if isinstance(destructible, TRexNew|TRexNewCave):
                if destructible.invincibility < 1:
                    destructible.health -= 1
                    destructible.invincibility = destructible.INVINCIBILITY_DURATION
                    destructible.vel_x = -destructible.VEL_X_MIN
                    destructible.vel_y = destructible.JUMP_ACCEL
            elif isinstance(destructible, LandMine):
                destructible.triggered_at = curr_ticks
            else:
                explosion = Explosion().instead_of(destructible)
                obj_container.queue_delete(destructible)
                obj_container.queue_add(explosion)

        obj.last_update = curr_ticks