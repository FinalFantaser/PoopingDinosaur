import random
import pygame.time
from objects import *
import core
from data_containers import objects as obj_container, game_data
from object_handlers.object_handler import ObjectHandler


class TRexHandler(ObjectHandler):
    _EDIBLES: tuple[type[Object], ...] = (
        Velociraptor,
        Austroraptor,
        Pterodactyl,
    )

    @classmethod
    def update(cls, obj: TRex) -> None:
        ground: Ground = obj_container.get(Ground.ID)
        update_delta: int = obj.update_delta

        # Movement
        obj.x += obj.vel_x_total / 1000 * update_delta

        if obj.rect.left <= ground.rect.left:
            obj.x = ground.rect.left
        elif obj.rect.right >= ground.rect.right:
            obj.rect.right = ground.rect.right

        if obj.rect.bottom < ground.touch_level:
            fall_accel: float = game_data.GRAVITY_PIXELS * obj.weight_factor()
            obj.vel_y += fall_accel/1000 * update_delta

        obj.y += obj.vel_y / 1000 * update_delta
        if obj.rect.bottom >= ground.touch_level:
            obj.vel_y = 0.0
            obj.rect.bottom = ground.touch_level

        # Normalizing vel_x_modifier
        if obj.vel_x_modifier != 0.0:
            accel: float = obj.VEL_X_MODIFIER/500 * update_delta

            if obj.vel_x_modifier < 0:
                obj.vel_x_modifier = min(obj.vel_x_modifier + accel, 0.0)
            else:
                obj.vel_x_modifier = max(0.0, obj.vel_x_modifier - accel)

        # Collision check
        for other_obj in obj_container.visible().values():
            # Skipping oneself
            if other_obj.id == obj.id or isinstance(other_obj, Ground):
                continue

            if obj.hitbox.overlaps(other_obj.rect):
                # Obstacles
                if isinstance(other_obj, Obstacle) and obj.invincibility < 1:
                    # Cactus
                    if other_obj.ob_type == Obstacle.Type.CACTUS:
                        obj.health = max(0, obj.health - 1)
                        obj.invincibility = 3000

                        obj.vel_x_modifier = -obj.VEL_X_MODIFIER * 6

                        # Throw back
                        if obj.rect.bottom >= ground.touch_level:
                            obj.vel_y = obj.BASE_JUMP_ACCEL/10 + obj.vel_x_modifier
                        else:
                            obj.vel_y = obj.BASE_JUMP_ACCEL/12 + obj.vel_x_modifier

                    # Thorns or ferns
                    elif other_obj.ob_type == Obstacle.Type.THORNS or other_obj.ob_type == Obstacle.Type.FERN:
                        # Slow down
                        obj.vel_x_modifier = -(obj.VEL_X_CONST / 2)

                        # Hurt if touching thorns
                        if other_obj.ob_type == Obstacle.Type.THORNS:
                            obj.health = max(0, obj.health - 1)
                            obj.invincibility = 3000

                            # Jump in pain
                            obj.vel_y = obj.BASE_JUMP_ACCEL/2.5


                    # Stone
                    elif other_obj.ob_type == Obstacle.Type.STONE:
                        if obj.rect.bottom >= ground.touch_level:
                            obj.vel_y = obj.BASE_JUMP_ACCEL/25 - obj.vel_x_modifier
                        else:
                            obj.vel_y = obj.BASE_JUMP_ACCEL/30 - obj.vel_x_modifier

                        obj.vel_x_modifier = obj.VEL_X_MODIFIER * 2.5

                    # Tree or skeleton
                    elif other_obj.ob_type == Obstacle.Type.TREE or other_obj.ob_type == Obstacle.Type.SKELETON:
                        obj.vel_x_modifier = -obj.VEL_X_MODIFIER * 6

                        # Bounce back
                        if obj.rect.bottom >= ground.touch_level:
                            obj.vel_y = obj.BASE_JUMP_ACCEL / 10 + obj.vel_x_modifier
                        else:
                            obj.vel_y = obj.BASE_JUMP_ACCEL / 12 + obj.vel_x_modifier

            # Edibles
            if isinstance(other_obj, cls._EDIBLES) and obj.poos < obj.MAX_POOS:
                if obj.action != TRexAction.BITE:
                    if obj.bite_hitbox.overlaps(other_obj.rect):
                        obj.action = TRexAction.BITE
                elif (
                        obj.hitbox.overlaps(other_obj.rect)
                        and obj.action == TRexAction.BITE
                        and obj.curr_frame == obj.ANIMATION_FRAMES[TRexAction.BITE] - 1
                ):
                    obj.poos += 1
                    obj.health = min(obj.health + 1, obj.MAX_HEALTH)
                    obj_container.queue_delete(other_obj)

        # Blink if invincible
        obj.invincibility = max(0, obj.invincibility - update_delta)
        if obj.invincibility > 0 and pygame.time.get_ticks() - obj.last_blink >= obj.BLINK_INTERVAL:
            obj.last_blink = pygame.time.get_ticks()
            obj.visible = not obj.visible

        if obj.invincibility < 1:
            obj.visible = True

        # Switch to run after the bite animation ends
        if obj.action == TRexAction.BITE:
            if obj.curr_frame >= obj.ANIMATION_FRAMES[obj.action] - 1 and pygame.time.get_ticks() - obj.last_frame_change >= obj.ANIM_INTERVAL:
                obj.action = TRexAction.RUN

        obj.last_update = pygame.time.get_ticks()


    @classmethod
    def read_input(cls, obj: TRex) -> None:
        ground: Ground = obj_container.get(Ground.ID)

        accel: float = obj.VEL_X_MODIFIER / 250 * obj.update_delta

        if core.input.held("left"):
            if obj.vel_x_modifier > -obj.VEL_X_MODIFIER:
                obj.vel_x_modifier = max(-obj.VEL_X_MODIFIER, obj.vel_x_modifier - accel)
        elif core.input.held("right"):
            if obj.vel_x_modifier < obj.VEL_X_MODIFIER:
                obj.vel_x_modifier = min(obj.vel_x_modifier + accel, obj.VEL_X_MODIFIER)

        if core.input.pressed("up") and obj.rect.bottom >= ground.touch_level:
            obj.vel_y = obj.BASE_JUMP_ACCEL * obj.weight_factor() - obj.vel_x_modifier
            obj.vel_x_modifier += max(obj.VEL_X_MODIFIER, obj.vel_x_modifier - accel)

        if (
                core.input.pressed("poop")
                and obj.poos > 0
                and pygame.time.get_ticks() - obj.last_pooped_at >= obj.POOP_INTERVAL
        ):
            obj.poos -= 1
            obj.last_pooped_at = pygame.time.get_ticks()
            obj_container.queue_add(
                Poo((obj.hitbox.left, obj.y), TRex.POO_WEIGHT)
            )

            if obj.rect.bottom >= ground.touch_level and obj.vel_y == 0.0:
                obj.vel_y = obj.BASE_JUMP_ACCEL/3 / obj.weight_factor() - obj.vel_x_modifier
            elif obj.vel_y >= 0:
                obj.vel_y = obj.BASE_JUMP_ACCEL/2 / obj.weight_factor() - obj.vel_x_modifier

            sound_key: str = random.choice(tuple(f"fart_{idx}" for idx in range(1, 3)))
            core.audio.sound_play(sound_key)
