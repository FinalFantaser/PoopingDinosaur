import random
from pygame.time import get_ticks

import core.input, core.audio
from objects import *
from data_containers import objects as obj_container, game_data
from .object_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler


class TRexNewHandler(ObjectHandler, DinosaurHandler):
    EDIBLE_DINOSAURS: tuple[type[Object], ...] = (
        Velociraptor,
        Austroraptor,
        Pterodactyl,
        # ...
    )

    @classmethod
    def update(cls, obj: TRexNew) -> None:
        cls.physics(obj)
        cls.read_input(obj)

        update_delta: int = obj.update_delta

        # Accelerating / Slowing down with no external impact
        if obj.vel_x < obj.VEL_X_MIN:
            accel_x: float = obj.ACCEL_X_PER_MICROSECOND * update_delta
            obj.vel_x = min(obj.vel_x + accel_x, obj.VEL_X_MIN)
        elif obj.vel_x > obj.VEL_X_MAX:
            accel_x: float = obj.ACCEL_X_PER_MICROSECOND * update_delta
            obj.vel_x = max(obj.vel_x - accel_x, obj.VEL_X_MIN)

        # Stop biting
        if (
            obj.state == obj.State.BITING
            and obj.curr_frame_head == obj.TOTAL_FRAMES_HEAD - 1
            and get_ticks() - obj.last_frame_change_head >= obj.ANIM_INTERVAL_HEAD
        ):
            obj.curr_frame_head = 0
            obj.state = obj.State.RUNNING

        # Reacting to environment
        trex_fov: Rect = obj.fov_ahead
        trex_hitbox: Rect = obj.hitbox
        trex_hitbox_bite: Rect = obj.hitbox_bite

        for other_obj in obj_container.visible().values():
            # Skipping oneself and ground
            if other_obj.id == obj.id or isinstance(other_obj, Ground):
                continue

            # Seeing edible dinosaurs
            if (
                    obj.state != obj.State.BITING
                    and trex_fov.overlaps(other_obj.rect)
                    and isinstance(other_obj, cls.EDIBLE_DINOSAURS)
            ):
                obj.state = obj.State.BITING

        obj.last_update = get_ticks()

    @classmethod
    def physics(cls, obj: TRexNew) -> None:
        cls.gravity(obj)

        # Horizontal movement
        total_vel_x: float = obj.vel_x + obj.vel_x_modifier
        obj.x += total_vel_x / 1000 * obj.update_delta * obj.direction.value[0]

    @classmethod
    def read_input(cls, obj: TRexNew) -> None:
        ground: Ground = obj_container.get_ground()
        update_delta: int = obj.update_delta
        accel_x: float = obj.ACCEL_X_MODIFIER_PER_MICROSECOND * update_delta


        if core.input.held("left"):
            obj.vel_x_modifier = max(obj.vel_x_modifier - accel_x, obj.VEL_X_MODIFIER_MIN)
        elif core.input.held("right"):
            obj.vel_x_modifier = min(obj.vel_x_modifier + accel_x, obj.VEL_X_MODIFIER_MAX)
        else:
            if obj.vel_x_modifier > 0:
                obj.vel_x_modifier = max(obj.vel_x_modifier - accel_x, obj.VEL_X_MODIFIER_MIN)
            else:
                obj.vel_x_modifier = min(obj.vel_x_modifier + accel_x, obj.VEL_X_MODIFIER_MAX)


        if core.input.pressed("up") and obj.rect.bottom >= ground.touch_level:
            obj.vel_y = obj.JUMP_ACCEL * obj.weight_factor - obj.vel_x_modifier + (obj.poos * obj.POO_WEIGHT)

        if (
            core.input.pressed("poop")
            and obj.poos > 0
            and get_ticks() - obj.last_pooped_at >= obj.POOP_INTERVAL
        ):
            obj.poos -= 1
            obj.last_pooped_at = get_ticks()
            obj_container.queue_add(
                Poo((obj.hitbox.left, obj.y), TRexNew.POO_WEIGHT)
            )

            # Kick up
            if obj.rect.bottom >= ground.touch_level and obj.vel_y == 0.0:
                obj.vel_y = obj.JUMP_ACCEL/3 / obj.weight_factor - obj.vel_x_modifier
            elif obj.vel_y >= 0:
                obj.vel_y = obj.JUMP_ACCEL/2 / obj.weight_factor - obj.vel_x_modifier

            sound_key: str = random.choice(tuple(f"fart_{idx}" for idx in range(1, 3)))
            core.audio.sound_play(sound_key)