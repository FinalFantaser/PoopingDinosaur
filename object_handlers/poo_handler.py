import pygame.time
from objects import Poo, Ground, Dinosaur, TRexNew
from object_handlers.object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class PooHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Poo) -> None:
        if cls.delete_if_passed_camera():
            return

        cls.gravity(obj)

        # Caching
        poo_hitbox = obj.rect

        # Collision with NPCs
        for npc in obj_container.visible().values():
            # Skip oneself, not in MAIN layer, TRex, not NPC, beyond reach
            if npc.id == obj.id or npc.LAYER != npc.Layer.MAIN or not isinstance(obj, Dinosaur) or isinstance(obj, TRexNew):
                continue

            npc_hitbox = obj.hitbox

            if not poo_hitbox.overlaps(npc_hitbox):
                continue

            # Flatten small NPCs if hitting from above
            # ...

            # Just Kill all heavier non-boss NPCs:
            # - Create explosion instead of an NPC
            # - Leave a skeleton instead of a bigger dinosaur
            # ...

            # Damage a boss NPC
            # ...

        obj.last_update = pygame.time.get_ticks()

    @classmethod
    def gravity(cls, obj: Poo) -> None:
        update_delta: int = obj.update_delta
        ground: Ground = obj_container.get_ground()

        if obj.rect.bottom < ground.touch_level:
            fall_accel: float = game_data.GRAVITY_PIXELS * obj.weight_factor
            obj.vel_y += fall_accel / 1000 * update_delta

        obj.y += obj.vel_y / 1000 * update_delta
        if obj.rect.bottom >= ground.touch_level:
            obj.vel_y = 0.0
            obj.rect.bottom = ground.touch_level