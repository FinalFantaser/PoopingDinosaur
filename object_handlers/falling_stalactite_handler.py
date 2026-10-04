from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Dinosaur, TRexNew, Explosion, FlattenedObject, FallingStalactite
from data_containers import objects as obj_container, game_data
from .object_handler import ObjectHandler


class FallingStalactiteHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: FallingStalactite):
        if cls.delete_if_passed_camera(obj):
            return

        cls.clear_unexistent_touches(obj)

        time_delta = obj.update_delta

        if obj.dead:
            if obj.is_falling:
                cls._process_falling_stalactite(obj)
            else:
                cls._process_dead_stalactite(obj)
        else:
            cls._process_live_stalactite(obj)

        obj.last_update = get_ticks()

    @classmethod
    def _process_falling_stalactite(cls, stalactite: FallingStalactite) -> None:
        cls.gravity(stalactite)

        # Explode when hits the ground
        if stalactite.rect.bottom >= obj_container.get_ground().touch_level:
            new_explosion = Explosion().instead_of(stalactite)

            obj_container.queue_delete(stalactite)
            obj_container.queue_add(new_explosion)
        # React to an NPC
        else:
            for other_obj in obj_container.main_layer().values():
                if not isinstance(other_obj, Dinosaur):
                    continue

                if other_obj.invincibility > 0:
                    continue

                if stalactite.rect.overlaps(other_obj.hitbox):
                    if cls.are_touching(stalactite, other_obj):
                        obj_container.queue_delete(stalactite)
                        obj_container.queue_add(Explosion().instead_of(stalactite))

                        cls.mark_as_touching(stalactite, other_obj)
                        other_obj.invincibility = other_obj.INVINCIBILITY_DURATION

                        # If it's T-Rex, bounce him back (or forth)
                        if isinstance(other_obj, TRexNew):
                            other_obj.health -= 1

                            dir_modifier = 1 if stalactite.rect.center_x > other_obj.hitbox.center_x else -1

                            other_obj.vel_x = other_obj.VEL_X_MIN * 0.5 * dir_modifier

                            if other_obj.vel_y >= 0:
                                other_obj.vel_y = other_obj.jump_impulse

                        # If a dinosaur is smol, Super Mario Bros the sucker
                        elif other_obj.weight < game_data.HEAVY_DINOSAUR_WEIGHT:
                            obj_container.queue_delete(other_obj)
                            obj_container.queue_add(FlattenedObject.instead_of(other_obj))
                        # Still, if you're not T-Rex, tough luck
                        else:
                            obj_container.queue_delete(other_obj)
                else:
                    cls.mark_as_not_touching(stalactite, other_obj)

    @classmethod
    def _process_dead_stalactite(cls, stalactite: FallingStalactite) -> None:
        """This stalactite hates T-Rex specifically"""
        trex: None|TRexNew = obj_container.get(TRexNew.ID)

        if trex is not None and stalactite.fall_trigger_area.overlaps(trex.hitbox):
            stalactite.is_falling = True

    @classmethod
    def _process_live_stalactite(cls, stalactite: FallingStalactite) -> None:
        """Alive stalactite just drips and gives zero fucks (just like any other senior)"""
        if stalactite.drop_exists:
            stalactite.drop_pos = (
                stalactite.drop_pos[0],
                stalactite.drop_pos[1] + stalactite.DROP_SPEED / 1000 * stalactite.update_delta,
            )

            if stalactite.drop_pos[1] >= obj_container.get_ground().touch_level:
                stalactite.drop_exists = False
                stalactite.last_dropped_at = get_ticks()

        elif get_ticks() - stalactite.last_dropped_at >= stalactite.DROP_INTERVAL:
            stalactite.drop_exists = True
            stalactite.drop_pos = stalactite.drop_pos[0], stalactite.rect.bottom + 1