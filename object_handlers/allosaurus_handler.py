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

        # Collision check
        for other_obj in obj_container.visible().values():
            if other_obj.id == obj.id or isinstance(other_obj, Ground):
                continue

            if obj.hitbox.overlaps(other_obj.rect):
                if isinstance(other_obj, Obstacle) and obj.invincibility < 1:
                    obj.vel_y -= obj.VEL_Y_MIN * (obj.total_weight / 3) + obj.vel_x_modifier
                    obj.invincibility = 3000
                    # TODO Снижение горизонтальной скорости

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

        if core.input.pressed("left"):
            obj.vel_x_modifier = -(obj.VEL_X_MODIFIER)
        elif core.input.pressed("right"):
            obj.vel_x_modifier = obj.VEL_X_MODIFIER
        else:
            obj.vel_x_modifier = 0.0

        if core.input.pressed("up") and obj.rect.bottom >= ground.touch_level:
            obj.vel_y -= obj.VEL_Y_MIN * (obj.total_weight / 3) + obj.vel_x_modifier