from typing import Callable
import random
from pygame.time import get_ticks

import core.input, core.audio
from data_containers.objects import dinosaurs
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

    REACTIONS_SEE: dict[Obstacle.Type, str|None] = {
        Obstacle.Type.CACTUS: None,
        Obstacle.Type.THORNS: None,
        Obstacle.Type.STONE: None,
        Obstacle.Type.TREE: None,
        Obstacle.Type.FERN: None,
        Obstacle.Type.SKELETON: None,
        # ... spicy berries
    }

    @classmethod
    def update(cls, obj: TRexNew) -> None:
        cls.physics(obj)
        cls.read_input(obj)

        update_delta: int = obj.update_delta

        trex_fov: Rect = obj.fov_ahead
        trex_hitbox: Rect = obj.hitbox
        trex_hitbox_bite: Rect = obj.hitbox_bite

        # Accelerating / Slowing down with no external impact
        if obj.vel_x < obj.VEL_X_MIN:
            if trex_hitbox.bottom >= obj_container.get_ground().touch_level:
                accel_x: float = obj.ACCEL_X_PER_MICROSECOND * update_delta
                obj.vel_x = min(obj.vel_x + accel_x, obj.VEL_X_MIN)
        elif obj.vel_x >= obj.VEL_X_MAX:
            accel_x: float = obj.ACCEL_X_PER_MICROSECOND * update_delta
            obj.vel_x = max(obj.vel_x - accel_x, obj.VEL_X_MAX)

        # Blink if invincible
        if obj.invincibility > 0:
            obj.invincibility = max(0, obj.invincibility - update_delta)
            if get_ticks() - obj.last_blink >= obj.BLINK_INTERVAL:
                obj.last_blink = get_ticks()
                obj.visible = not obj.visible
        else:
            obj.visible = True

        # Stop biting
        if (
            obj.state == obj.State.BITING
            and obj.curr_frame_head == obj.TOTAL_FRAMES_HEAD - 1
            and get_ticks() - obj.last_frame_change_head >= obj.calc_anim_interval(obj.ANIM_INTERVAL_HEAD)
        ):
            obj.curr_frame_head = 0
            obj.last_frame_change_head = get_ticks()
            obj.state = obj.State.RUNNING

        # Reacting to environment
        for other_obj in obj_container.visible().values():
            # Skipping non-MAIN layer, oneself, ground
            if other_obj.LAYER != obj.LAYER or other_obj.id == obj.id or isinstance(other_obj, Ground):
                continue

            # Seeing edible dinosaurs
            if (
                    obj.state != obj.State.BITING
                    and obj.poos < obj.MAX_POOS
                    and trex_fov.overlaps(other_obj.rect)
                    and isinstance(other_obj, cls.EDIBLE_DINOSAURS)
            ):
                obj.state = obj.State.BITING

            # Biting edible dinosaurs
            if (
                obj.state == obj.State.BITING
                and obj.poos < obj.MAX_POOS
                and obj.curr_frame_head >= obj.TOTAL_FRAMES_HEAD - 1
                and isinstance(other_obj, cls.EDIBLE_DINOSAURS)
                and trex_hitbox_bite.overlaps(other_obj.rect)
            ):
                other_obj.health -= 1

                # Other dinosaur dies if hp below zero (yeah no shit)
                if other_obj.health <= 0:
                    obj_container.queue_delete(other_obj)

                    # Eat smaller dinosaur (don't leave skeleton) and restore health & poos
                    if other_obj.weight < game_data.HEAVY_DINOSAUR_WEIGHT:
                        obj.health = min(obj.health + other_obj.HEALTH_MAX, obj.HEALTH_MAX)
                        obj.poos = min(obj.poos + other_obj.HEALTH_MAX, obj.MAX_POOS)
                    else: # Leave skeleton
                        die_explosion: Explosion = Explosion(
                            spawn=Obstacle.make_skeleton(other_obj)
                        ).instead_of(other_obj)

                        obj_container.queue_add(die_explosion)
                # Other dinosaur bounces forward if not killed
                else:
                    obj.vel_x += obj.vel_x * 0.25
                    obj.vel_y -= obj.JUMP_ACCEL * 0.25

            # Skipping obstacles and NPCs if invincible
            if obj.invincibility > 0:
                continue

            # Collision with dinosaurs (bouncing)
            if isinstance(other_obj, Dinosaur) and trex_hitbox.overlaps(other_obj.hitbox):
                cls.react_to_dinosaur(obj, other_obj)

            # Obstacles
            if isinstance(other_obj, Obstacle):
                cls.react_to_obstacles(obj, other_obj)

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
            if obj.hitbox.bottom >= ground.touch_level:
                obj.vel_x_modifier = max(obj.vel_x_modifier - accel_x, obj.VEL_X_MODIFIER_MIN)
        elif core.input.held("right"):
            if obj.hitbox.bottom >= ground.touch_level:
                obj.vel_x_modifier = min(obj.vel_x_modifier + accel_x, obj.VEL_X_MODIFIER_MAX)
        else:
            if obj.vel_x_modifier > 0:
                obj.vel_x_modifier = max(obj.vel_x_modifier - accel_x, obj.VEL_X_MODIFIER_DEFAULT)
            else:
                obj.vel_x_modifier = min(obj.vel_x_modifier + accel_x, obj.VEL_X_MODIFIER_DEFAULT)


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

    @classmethod
    def react_to_dinosaur(cls, trex: TRexNew, dinosaur: Dinosaur) -> None:
        # If a dinosaur is smol, Super Mario Brothers the sucker
        if dinosaur.weight < game_data.HEAVY_DINOSAUR_WEIGHT:
            flatten_hitbox = trex.hitbox_flatten
            dinosaur_hitbox = dinosaur.hitbox

            if (
                    trex.vel_y > 0
                    and flatten_hitbox.overlaps(dinosaur_hitbox)
                    and flatten_hitbox.bottom >= dinosaur_hitbox.top - dinosaur_hitbox.height / 3
                    and dinosaur.rect.bottom >= obj_container.get_ground().touch_level
            ):
                obj_container.queue_delete(dinosaur)
                obj_container.queue_add(FlattenedObject.instead_of(dinosaur))
        # Otherwise, bounce
        else:
            cls.bounce_back(trex, dinosaur)

    @classmethod
    def cactus_touch(cls, dinosaur: Dinosaur, cactus: Obstacle) -> None:
        pass

    @classmethod
    def thorns_touch(cls, dinosaur: TRexNew, thorns: Obstacle) -> None:
        # Slow down
        dinosaur.vel_x_modifier = dinosaur.VEL_X_MODIFIER_MIN

        # Hurt
        dinosaur.health -= 1
        dinosaur.invincibility = dinosaur.INVINCIBILITY_DURATION

        # Jump in pain
        dinosaur.vel_y = dinosaur.JUMP_ACCEL * 0.1

    @classmethod
    def stone_touch(cls, dinosaur: TRexNew, stone: Obstacle) -> None:
        if dinosaur.hitbox.bottom >= obj_container.get_ground().touch_level:
            dinosaur.vel_y = dinosaur.JUMP_ACCEL * 0.3
        else:
            dinosaur.vel_y = dinosaur.JUMP_ACCEL * 0.5

        dinosaur.vel_x_modifier = dinosaur.VEL_X_MODIFIER_MAX * 1.5


    @classmethod
    def tree_touch(cls, dinosaur: TRexNew, tree: Obstacle) -> None:
        direction = -1 if tree.rect.center_x >= dinosaur.hitbox.center_x else 1
        dinosaur.vel_x = dinosaur.VEL_X_MIN * 0.5 * direction + dinosaur.vel_x * direction * 0.25
        dinosaur.vel_x_modifier = dinosaur.VEL_X_MODIFIER_MIN
        dinosaur.vel_y = dinosaur.JUMP_ACCEL


    @classmethod
    def fern_touch(cls, dinosaur: Dinosaur, fern: Obstacle) -> None:
        pass

    @classmethod
    def skeleton_touch(cls, dinosaur: Dinosaur, skeleton: Obstacle) -> None:
        pass