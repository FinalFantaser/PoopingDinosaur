import pygame.time
from objects import *
import core.input
from data_containers import objects as obj_container
from object_handlers.object_handler import ObjectHandler


class AllosaurusHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Allosaurus) -> None:
        ground: Ground = obj_container.get(Ground.ID)

        obj.x += obj.vel_x / 1000 * obj.update_delta

        if obj.rect.left <= ground.rect.left:
            obj.x = ground.rect.left
        elif obj.rect.right >= ground.rect.right:
            obj.rect.right = ground.rect.right

        if obj.rect.bottom < ground.touch_level:
            obj.vel_y = min(Allosaurus.MAX_VEL_Y, obj.vel_y + 0.2)

        obj.y += obj.vel_y / 1000 * obj.update_delta
        if obj.rect.bottom >= ground.touch_level:
            obj.vel_y = 0.0
            obj.rect.bottom = ground.touch_level

        obj.last_update = pygame.time.get_ticks()

    @classmethod
    def read_input(cls, obj: Allosaurus) -> None:
        if core.input.pressed("left"):
            obj.direction = obj.DIR_LEFT
            accel = obj.MAX_VEL_X / 1000 / 4  * obj.update_delta * obj.direction
            obj.vel_x = max(obj.MAX_VEL_X * obj.direction, obj.vel_x + accel)

        if core.input.pressed("right"):
            obj.direction = obj.DIR_RIGHT
            accel = obj.MAX_VEL_X / 1000 / 4 * obj.update_delta * obj.direction
            obj.vel_x = min(obj.MAX_VEL_X * obj.direction, obj.vel_x + accel)