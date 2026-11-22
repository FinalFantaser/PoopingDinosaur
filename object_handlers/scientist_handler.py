from random import randint
from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Scientist
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class ScientistHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Scientist):
        curr_ticks = get_ticks()

        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        if obj.state == obj.State.IDLE:
            trex_hitbox = obj_container.get_player().hitbox
            if trex_hitbox.overlaps(obj.fov):
                obj.state = obj.State.STARTLED
                obj.vel_y = obj.JUMP_ACCEL

        elif obj.state == obj.State.STARTLED:
            if obj.rect.bottom >= obj_container.get_ground().touch_level:
                obj.state = obj.State.RUNNING

        else: # Running
            if curr_ticks >= obj.next_direction_change:
                obj.direction = obj.direction.opposite()
                obj.next_direction_change = curr_ticks + randint(*obj.DIRECTION_CHANGE_INTERVAL)

            obj.vel_x = obj.VEL_X * obj.direction.value[0]

            if obj.rect.bottom >= obj_container.get_ground().touch_level:
                obj.vel_y = obj.JUMP_ACCEL/2

        obj.last_update = curr_ticks
