from random import randint
from pygame.time import get_ticks
from pygame.mask import Mask
from objects import Direction, Jeep, Bullet, Explosion, Human, TRexNew, Skyscraper, Dinosaur, FlattenedObject
from .object_handler import ObjectHandler
from data_containers import objects as obj_container


class JeepHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Jeep):
        print(f"{obj.id}")

        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        curr_time = get_ticks()

        # Shoot
        if curr_time >= obj.next_shot_at:
            obj.next_shot_at = curr_time + randint(*obj.SHOOT_INTERVAL)
            bullet = Bullet(
                (obj.x - Bullet.WIDTH, obj.y),
                Direction.LEFT
            )
            obj_container.queue_add(bullet)

        # Collision check
        for other_obj in obj_container.main_layer().values():
            if not isinstance(other_obj, (Skyscraper, Dinosaur, Human)):
                continue

            if not obj.rect.overlaps(getattr(other_obj, "hitbox", other_obj.rect)):
                continue

            if isinstance(other_obj, TRexNew):
                if other_obj.invincibility < 1:
                    other_obj.health -= 1
                    other_obj.invincibility = other_obj.INVINCIBILITY_DURATION
                    other_obj.vel_x = -other_obj.VEL_X_MIN
                    other_obj.vel_y = other_obj.JUMP_ACCEL/2

                    explosion = Explosion().instead_of(obj)
                    obj_container.queue_delete(obj)
                    obj_container.queue_add(explosion)
            elif isinstance(other_obj, Skyscraper):
                collision = False

                if other_obj.health == other_obj.MAX_HEALTH:
                    collision = True
                elif other_obj.health > 0:
                    jeep_mask = Mask(obj.size, True)
                    offset = other_obj.x - obj.x, other_obj.y - obj.y
                    collision = jeep_mask.overlap(other_obj.bit_mask, offset)

                if collision:
                    explosion = Explosion().instead_of(obj)
                    obj_container.queue_delete(obj)
                    obj_container.queue_add(explosion)
            elif isinstance(other_obj, Human): # Experimental
                flattened = FlattenedObject.instead_of(other_obj)
                obj_container.queue_delete(other_obj)
                obj_container.queue_add(flattened)

        obj.last_update = get_ticks()

