import math

from pygame.mask import Mask
from pygame.time import get_ticks
from objects import Missile, Explosion, Helicopter, Skyscraper, Object
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class MissileHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Missile):
        cls.delete_if_passed_camera(obj)
        cls.track_target(obj)
        cls.physics(obj)
        cls.collisions(obj)

        obj.last_update = get_ticks()

    @classmethod
    def delete_if_passed_camera(cls, obj: Missile) -> bool:
        if obj.target_id is not None and obj.hitbox.bottom < obj_container.get_camera().top:
            obj_container.queue_delete(obj)
            return True

        return False

    @classmethod
    def track_target(cls, missile: Missile) -> None:
        if missile.target_id is None:
            helicopter = obj_container.filter(
                obj_container.Filter().by_type(Helicopter).limit_by(1)
            )

            if helicopter is not None:
                missile.target_id = helicopter.id

        if missile.target_id is None:
            return

        target = obj_container.get(missile.target_id, False)
        if target is None:
            missile.target_id = None
            return

        delta_x = target.x - missile.x
        delta_y = target.y - missile.y
        target_angle = math.degrees(math.atan2(delta_y, delta_x))

        diff = (target_angle - missile.angle + 180) % 360 - 180

        max_turn = missile.ROTATION_SPEED / 1000 * missile.update_delta
        turn = max(-max_turn, min(diff, max_turn))

        missile.angle += turn

    @classmethod
    def physics(cls, obj: Missile) -> None:
        delta_time = obj.update_delta
        rad = math.radians(obj.angle)

        obj.vel_x = obj.SPEED * math.cos(rad)
        obj.vel_y = obj.SPEED * math.sin(rad)

        obj.x += obj.vel_x * delta_time / 1000
        obj.y += obj.vel_y * delta_time / 1000

    @classmethod
    def collisions(cls, missile: Missile) -> None:
        for other_obj in obj_container.visible().values():
            if not isinstance(other_obj, (Helicopter, Skyscraper)):
                continue

            if not missile.hitbox.overlaps(other_obj.rect):
                continue

            if isinstance(other_obj, Helicopter):
                explosion = Explosion().instead_of(missile)
                obj_container.queue_add(explosion)
                obj_container.queue_delete(missile)
                obj_container.queue_delete(other_obj)
            elif isinstance(other_obj, Skyscraper):
                if other_obj.health > 0:
                    if other_obj.health == other_obj.MAX_HEALTH:
                        explosion = Explosion().instead_of(missile)
                        obj_container.queue_add(explosion)
                        obj_container.queue_delete(missile)
                        other_obj.health -= 1
                    else:
                        mask = Mask(missile.curr_size, True)
                        offset = other_obj.x - missile.x, other_obj.y - missile.y

                        if mask.overlap(other_obj.bit_mask, offset):
                            explosion = Explosion().instead_of(missile)
                            obj_container.queue_add(explosion)
                            obj_container.queue_delete(missile)
                            other_obj.health -= 1
