from pygame.time import get_ticks
from objects import (
    Skeleton,
    Explosion,
    Dinosaur,
    TRexNew,
    Bullet,
    Skyscraper,
    Tesla,
    Helicopter,
    # Jeep,
    Human,
)
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data
from data_containers.objects import Filter as ObjectFilter


class BulletHandler(ObjectHandler):
    DESTRUCTIBLES: tuple[type[Dinosaur|Human], ...] = (
        Dinosaur,
        Human,
    )

    @classmethod
    def update(cls, obj: Bullet):
        if cls.delete_if_passed_camera(obj):
            return

        time_delta = obj.update_delta

        obj_filter = ObjectFilter().by_type((
            Dinosaur,
            TRexNew,
            Skyscraper,
            Tesla,
            Helicopter,
            # Jeep,
            Human,
        )).limit_by(100).return_as(tuple)


        obj.x += obj.VEL_X * obj.direction.value[0] / 1000 * time_delta

        for target in obj_container.filter(obj_filter):
            if not obj.rect.overlaps(getattr(target, "hitbox", target.rect)):
                continue

            if isinstance(target, TRexNew):
                if target.invincibility < 1:
                    target.health -= 1
                    target.invincibility = target.INVINCIBILITY_DURATION
                    target.vel_y = target.JUMP_ACCEL/2
                    target.vel_x = target.vel_x * obj.direction.value[0]

            elif isinstance(target, cls.DESTRUCTIBLES):
                explosion = Explosion().instead_of(target)
                if isinstance(target, Dinosaur) and target.weight >= game_data.HEAVY_DINOSAUR_WEIGHT:
                    explosion.spawn = Skeleton(target.id).instead_of(explosion)

                obj_container.queue_delete(target)
                obj_container.queue_add(explosion)

            else:
                obj_container.queue_delete(obj)

        obj.last_update = get_ticks()