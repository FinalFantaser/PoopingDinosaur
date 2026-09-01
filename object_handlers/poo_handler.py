import pygame.time
from objects import Poo, Ground, Dinosaur, TRexNew, FlattenedObject, Explosion, Obstacle
from object_handlers.object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class PooHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Poo) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        cls.gravity(obj)

        # Caching
        poo_hitbox = obj.rect

        # Collision with NPCs
        for npc in obj_container.visible().values():
            # Skip oneself, not in MAIN layer, TRex, not NPC
            if npc.id == obj.id or npc.LAYER != npc.Layer.MAIN or not isinstance(npc, Dinosaur) or isinstance(npc, TRexNew):
                continue

            npc_hitbox = npc.hitbox

            # Skip ones beyond reach
            if not poo_hitbox.overlaps(npc_hitbox):
                continue

            # Damage a boss NPC
            # Per each boss individually ...
            # ...


            # Hitting NPCs
            if isinstance(npc, Dinosaur): # ... and human NPCs on foot
                if npc.weight < game_data.HEAVY_DINOSAUR_WEIGHT:
                    # Flatten a smaller NPC when hitting from above
                    if (
                            obj.vel_y > 0
                            and poo_hitbox.bottom >= npc_hitbox.top - npc_hitbox.height / 3
                            and npc_hitbox.bottom >= obj_container.get_ground().touch_level
                    ):
                        obj_container.queue_delete(npc)
                        obj_container.queue_add(FlattenedObject.instead_of(npc))
                        continue
                    else: # Kill the poor bastard
                        npc.die()

                else: # Kill heavy dinosaurs and spawn skeletons:
                    explosion = Explosion(
                        spawn=Obstacle.make_skeleton(npc)
                    ).instead_of(npc)

                    obj_container.queue_delete(obj)
                    obj_container.queue_delete(npc)
                    obj_container.queue_add(explosion)

            # Explode vehicles ...
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