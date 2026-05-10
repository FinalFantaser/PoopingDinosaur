import pygame.time
from objects import *
import core.video
import core.input
from data_containers import objects as obj_container
from object_handlers.object_handler import ObjectHandler


class AllosaurusHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Allosaurus) -> None:
        ground: Ground = obj_container.get(Ground.ID)
        update_delta: int = obj.update_delta

        # Movement
        obj.x += obj.vel_x_total / 1000 * update_delta

        if obj.rect.left <= ground.rect.left:
            obj.x = ground.rect.left
        elif obj.rect.right >= ground.rect.right:
            obj.rect.right = ground.rect.right

        if obj.rect.bottom < ground.touch_level:
            obj.vel_y += obj.total_weight / 2

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
            if other_obj.id == obj.id or isinstance(other_obj, Ground):
                continue

            if obj.hitbox.overlaps(other_obj.rect):
                if isinstance(other_obj, Obstacle) and other_obj.ob_type == ObstacleType.CACTUS and obj.invincibility < 1:
                    obj.health = max(0, obj.health - 1)
                    obj.invincibility = 3000

                    obj.vel_x_modifier = -obj.VEL_X_MODIFIER * 6

                    if obj.rect.bottom >= ground.touch_level:
                        obj.vel_y -= obj.VEL_Y_MIN * (obj.total_weight / 3) + obj.vel_x_modifier
                    else:
                        obj.vel_y -= obj.VEL_Y_MIN

        # Blink if invincible
        obj.invincibility = max(0, obj.invincibility - update_delta)
        if obj.invincibility > 0 and pygame.time.get_ticks() - obj.last_blink >= obj.BLINK_INTERVAL:
            obj.last_blink = pygame.time.get_ticks()
            obj.visible = not obj.visible

        if obj.invincibility < 1:
            obj.visible = True

        obj.last_update = pygame.time.get_ticks()


    @classmethod
    def read_input(cls, obj: Allosaurus) -> None:
        ground: Ground = obj_container.get(Ground.ID)

        accel: float = obj.VEL_X_MODIFIER / 250 * obj.update_delta

        if core.input.held("left"):
            if obj.vel_x_modifier > -obj.VEL_X_MODIFIER:
                obj.vel_x_modifier = max(-obj.VEL_X_MODIFIER, obj.vel_x_modifier - accel)
        elif core.input.held("right"):
            if obj.vel_x_modifier < obj.VEL_X_MODIFIER:
                obj.vel_x_modifier = min(obj.vel_x_modifier + accel, obj.VEL_X_MODIFIER)

        if core.input.pressed("up") and obj.rect.bottom >= ground.touch_level:
            obj.vel_y -= obj.VEL_Y_MIN * (obj.total_weight / 3) + obj.vel_x_modifier
            obj.vel_x_modifier += max(obj.VEL_X_MODIFIER, obj.vel_x_modifier - accel)

        if (
                core.input.pressed("poop")
                and obj.poos > 0
                and pygame.time.get_ticks() - obj.last_pooped_at >= obj.POOP_INTERVAL
        ):
            obj.last_pooped_at = pygame.time.get_ticks()

            if obj.rect.bottom >= ground.touch_level and obj.vel_y == 0.0:
                obj.vel_y -= (obj.VEL_Y_MIN * (obj.total_weight / 3) + obj.vel_x_modifier)/2
            elif obj.vel_y >= 0:
                obj.vel_y = -(obj.VEL_Y_MIN * (obj.total_weight / 3) + obj.vel_x_modifier)/1.5

            obj.poos -= 1

            obj_container.queue_add(
                Poo((obj.hitbox.left, obj.y))
            )