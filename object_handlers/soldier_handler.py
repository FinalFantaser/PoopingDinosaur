from random import randint
from pygame.time import get_ticks
from objects import Direction, Soldier, Bullet
from .object_handler import ObjectHandler
from data_containers import objects as obj_container


class SoldierHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Soldier):
        curr_ticks = get_ticks()

        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        if obj.state == obj.State.IDLE:
            obj.vel_x = 0
            trex_hitbox = obj_container.get_player().hitbox
            if trex_hitbox.overlaps(obj.fov):
                obj.state = obj.State.STARTLED
                obj.vel_y = obj.JUMP_ACCEL
        elif obj.state == obj.State.STARTLED:
            obj.vel_x = 0
            if obj.rect.bottom >= obj_container.get_ground().touch_level:
                obj.state = obj.State.RUNNING
                obj.next_shot_at = curr_ticks + randint(*obj.SHOOT_INTERVAL)
        elif obj.state == obj.State.RUNNING:
            trex_hitbox = obj_container.get_player().hitbox

            obj.vel_x = obj.VEL_X * obj.direction.value[0]
            if obj.rect.bottom >= obj_container.get_ground().touch_level:
                obj.vel_y = obj.JUMP_ACCEL/2

            if obj.rect.center_x <= trex_hitbox.center_x:
                obj.direction = Direction.LEFT
            else:
                obj.direction = Direction.RIGHT

                if curr_ticks >= obj.next_shot_at:
                    obj.curr_frame = 0
                    obj.direction = Direction.LEFT
                    obj.state = obj.State.SHOOTING
        else:  # Shooting
            obj.vel_x = 0
            if obj.curr_frame >= obj.total_frames - 1 and curr_ticks - obj.last_frame_change >= obj.anim_interval:
                obj.next_shot_at = curr_ticks + randint(*obj.SHOOT_INTERVAL)

                bullet_vel_modifier = -1 if obj.direction == Direction.LEFT else 1

                bullet = Bullet((
                    (obj.x - Bullet.WIDTH) if obj.direction == Direction.LEFT else (obj.rect.right + 1),
                    obj.y,
                ))

                obj_container.queue_add(bullet)

                obj.state = obj.State.RUNNING

        obj.last_update = curr_ticks

