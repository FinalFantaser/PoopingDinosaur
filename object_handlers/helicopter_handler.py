from pygame.mask import Mask
from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Helicopter, TRexNew, Skyscraper, Explosion, Bomb
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class HelicopterHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Helicopter):
        cls.delete_if_passed_camera(obj)

        time_delta = obj.update_delta
        trex = obj_container.get(TRexNew.ID, True)

        # Behaviour
        cls.track_target(obj, trex, time_delta)
        cls.maintain_altitude(obj, time_delta)
        cls.drop_bomb(obj, trex)

        # Collision check
        cls.collisions(obj)

        # Physics
        cls.physics_ext(obj, time_delta)

        obj.last_update = get_ticks()

    @classmethod
    def delete_if_passed_camera(cls, obj: Helicopter) -> bool:
        if obj.bombs < 1 and obj.rect.bottom <= 0:
            obj_container.queue_delete(obj)
            return True

        return False

    @classmethod
    def track_target(cls, helicopter: Helicopter, trex: TRexNew, time_delta: int) -> None:
        if helicopter.rect.center_x < trex.rect.center_x + helicopter.TARGET_TRACKING_MIN:
            helicopter.engine_power_x = min(
                helicopter.ENGINE_POWER_X_MAX,
                helicopter.engine_power_x + helicopter.ENGINE_POWER_X * time_delta,
            )
        elif helicopter.rect.center_x > trex.rect.center_x + helicopter.TARGET_TRACKING_MAX:
            helicopter.engine_power_x = max(
                helicopter.ENGINE_POWER_X_MIN,
                helicopter.engine_power_x - helicopter.ENGINE_POWER_X * time_delta,
            )

    @classmethod
    def maintain_altitude(cls, helicopter: Helicopter, time_delta: int) -> None:
        if helicopter.bombs < 1:
            helicopter.engine_power_y = max(
                helicopter.ENGINE_POWER_Y_MIN,
                helicopter.engine_power_y - helicopter.ENGINE_POWER_Y * time_delta,
            )
            return

        if helicopter.y < helicopter.ALTITUDE_MAX:
            helicopter.engine_power_y = min(
                helicopter.ENGINE_POWER_Y_MAX,
                helicopter.engine_power_y + helicopter.ENGINE_POWER_Y * time_delta,
            )

        elif helicopter.y > helicopter.ALTITUDE_MIN:
            helicopter.engine_power_y = max(
                helicopter.ENGINE_POWER_Y_MIN,
                helicopter.engine_power_y - helicopter.ENGINE_POWER_Y * time_delta,
            )

    @classmethod
    def drop_bomb(cls, helicopter: Helicopter, trex: TRexNew) -> None:
        if helicopter.bombs < 1:
            return

        if helicopter.rect.center_x < trex.rect.center_x + helicopter.width * 2:
            return

        if helicopter.next_bomb_at <= get_ticks():
            helicopter.drop_bomb()
            bomb = Bomb(
                (helicopter.rect.center_x - Bomb.WIDTH/2, helicopter.rect.bottom),
                helicopter.vel_x,
            )
            obj_container.queue_add(bomb)

    @classmethod
    def collisions(cls, helicopter: Helicopter) -> None:
        for other_object in obj_container.main_layer().values():
            if not isinstance(other_object, (TRexNew, Skyscraper)):
                continue

            hitbox = getattr(other_object, "hitbox", other_object.rect)

            if not helicopter.rect.overlaps(hitbox):
                continue

            if isinstance(other_object, TRexNew):
                if other_object.invincibility < 1:
                    other_object.health -= 1
                    other_object.vel_x = -other_object.VEL_X_MIN
                    other_object.vel_y = other_object.JUMP_ACCEL
                    other_object.invincibility = other_object.INVINCIBILITY_DURATION

                    explosion = Explosion().instead_of(helicopter)
                    obj_container.queue_delete(helicopter)
                    obj_container.queue_add(explosion)
            elif isinstance(other_object, Skyscraper):
                if other_object.health > 0:
                    # ... pixel-perfect collision check
                    # ...
                    collision = True
                    if other_object.health < other_object.max_health:
                        mask = Mask(helicopter.size, True)
                        offset = other_object.x - helicopter.x, other_object.y - helicopter.y
                        collision = mask.overlap(other_object.bit_mask, offset)

                    if collision:
                        other_object.health -= 1
                        explosion = Explosion().instead_of(helicopter)
                        obj_container.queue_delete(helicopter)
                        obj_container.queue_add(explosion)

    @classmethod
    def physics_ext(cls, helicopter: Helicopter, time_delta: int) -> None:
        helicopter.vel_x = helicopter.VEL_X_MIN * helicopter.engine_power_x
        helicopter.vel_y = helicopter.VEL_Y_CONST * helicopter.engine_power_y

        cls.physics(helicopter)