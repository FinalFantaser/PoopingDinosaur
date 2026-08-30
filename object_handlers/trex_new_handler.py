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
    EDIBLE_DINOSAURS: tuple[type[Dinosaur], ...] = (
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
                and obj.curr_frame_head == obj.TOTAL_FRAMES_HEAD - 1
                and obj.poos < obj.MAX_POOS
                and isinstance(other_obj, cls.EDIBLE_DINOSAURS)
                and trex_hitbox_bite.overlaps(other_obj.hitbox)
            ):
                other_obj.health -= 1

                # Other dinosaur dies if hp below zero (yeah no shit)
                if other_obj.health <= 0:
                    obj_container.queue_delete(other_obj)

                    # Eat smaller dinosaur (don't leave skeleton) and restore health & poos
                    if other_obj.weight < game_data.HEAVY_DINOSAUR_WEIGHT:
                        obj.heal(1)
                        obj.poos = min(obj.poos + other_obj.HEALTH_MAX, obj.MAX_POOS)
                    else: # Leave skeleton
                        die_explosion: Explosion = Explosion(
                            spawn=Obstacle.make_skeleton(other_obj)
                        ).instead_of(other_obj)

                        obj_container.queue_add(die_explosion)
                # Other dinosaur bounces forward if not killed
                else:
                    other_obj.vel_x *= obj.vel_x * 1.5
                    other_obj.vel_y = min(obj.vel_y, obj.JUMP_ACCEL * 0.25)

            # Skipping obstacles and NPCs if invincible
            if obj.invincibility > 0:
                continue

            # Collision with dinosaurs
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
        vel_x_modifier = obj.vel_x_modifier

        if vel_x_modifier >= obj.VEL_X_MODIFIER_MIN and obj.vel_x >= obj.VEL_X_MAX:
            vel_x_modifier = 0

        total_vel_x: float = obj.total_vel_x + vel_x_modifier

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
            obj.vel_y = obj.jump_impulse

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
    def cactus_touch(cls, dinosaur: TRexNew, cactus: Obstacle) -> None:
        # Hurt
        dinosaur.health -= 1
        dinosaur.invincibility = dinosaur.INVINCIBILITY_DURATION

        # If jumping on the cactus, boost
        cls.bounce(
            dinosaur,
            cactus,
            cactus.rect.center_x > dinosaur.hitbox.center_x,
            dinosaur.vel_x * 1.25,
            dinosaur.jump_impulse if dinosaur.vel_y > 0 else None
        )


    @classmethod
    def thorns_touch(cls, dinosaur: TRexNew, thorns: Obstacle) -> None:
        # Slow down
        cls.fern_touch(dinosaur, thorns)

        # Hurt
        dinosaur.health -= 1
        dinosaur.invincibility = dinosaur.INVINCIBILITY_DURATION

        # Jump in pain
        if dinosaur.vel_y >= 0:
            dinosaur.vel_y = dinosaur.jump_impulse * 0.5

    @classmethod
    def stone_touch(cls, dinosaur: TRexNew, stone: Obstacle) -> None:
        # TRex can go past stones safely if threading slowly (also, ignore when thrown bock)
        vel_x_modifier = dinosaur.vel_x_modifier

        if vel_x_modifier >= dinosaur.VEL_X_MODIFIER_MIN and dinosaur.vel_x >= dinosaur.VEL_X_MAX:
            vel_x_modifier = 0

        total_vel_x = dinosaur.total_vel_x + vel_x_modifier

        if total_vel_x <= dinosaur.VEL_X_MIN:
            return

        vel_x = dinosaur.vel_x
        vel_y = None

        if dinosaur.hitbox.bottom >= obj_container.get_ground().touch_level:
            vel_y = dinosaur.JUMP_ACCEL * 0.3
        else:
            vel_y = dinosaur.JUMP_ACCEL * 0.5

        vel_x *= 1.2

        cls.bounce(dinosaur, stone, False, vel_x, vel_y)


    @classmethod
    def tree_touch(cls, dinosaur: TRexNew, tree: Obstacle) -> None:
        cls.bounce(
            dinosaur,
            tree,
            tree.rect.center_x > dinosaur.hitbox.center_x,
            dinosaur.vel_x * 1.2,
            dinosaur.jump_impulse if dinosaur.vel_y >= 0 else dinosaur.vel_y,
        )

        dinosaur.vel_x_modifier = dinosaur.VEL_X_MODIFIER_MIN


    @classmethod
    def fern_touch(cls, dinosaur: TRexNew, fern: Obstacle) -> None:
        dinosaur.vel_x = min(dinosaur.vel_x, dinosaur.VEL_X_MIN/2)

    @classmethod
    def skeleton_touch(cls, dinosaur: TRexNew, skeleton: Obstacle) -> None:
        trex_hitbox = dinosaur.hitbox
        skeleton_hitbox = skeleton.rect

        # If falling from above, boost (always go forward)
        if (
                dinosaur.vel_y >= 0
                and trex_hitbox.bottom < obj_container.get_ground().touch_level
                and trex_hitbox.bottom <= skeleton_hitbox.top
        ):
            vel_x = dinosaur.vel_x * 1.25
            vel_y = dinosaur.jump_impulse / 4

            cls.bounce(dinosaur, skeleton, False, vel_x, vel_y)
        else: # Bounce back
            cls.bounce_back(dinosaur, skeleton)


        # Destroy the skeleton
        explosion = Explosion().instead_of(skeleton)
        obj_container.queue_delete(skeleton)
        obj_container.queue_add(explosion)

    @classmethod
    def bounce(
            cls,
            dinosaur: TRexNew,
            obstacle: Obstacle|Dinosaur,
            opposite_dir: bool,
            override_vel_x: float | None = None,
            override_jump: float | None = None,
    ) -> None:
        vel_x = override_vel_x if override_vel_x is not None else dinosaur.total_vel_x / 5
        vel_y = override_jump

        if vel_y is None:
            jump_impulse = dinosaur.JUMP_ACCEL * dinosaur.weight_factor - dinosaur.vel_x_modifier
            poo_penalty = dinosaur.poos * dinosaur.POO_WEIGHT
            vel_y = (jump_impulse + poo_penalty) / 4

        cur_vel_modifier = 1 if vel_x >= 0 else -1
        limited_vel = min(dinosaur.VEL_X_MAX * 1.65, abs(vel_x)) * cur_vel_modifier


        dinosaur.vel_x = limited_vel * (-1 if opposite_dir else 1)
        dinosaur.vel_y = vel_y


    @classmethod
    def bounce_back(
            cls,
            dinosaur: TRexNew,
            obstacle: Obstacle|Dinosaur,
            override_vel_x: float | None = None,
            override_jump: float | None = None,
    ) -> None:
        cls.bounce(dinosaur, obstacle, True, override_vel_x, override_jump)