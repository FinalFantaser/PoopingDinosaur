from pygame.time import get_ticks

from objects import Camera, Obstacle, Dinosaur, TRex, TRexNew, Triceratops, Velociraptor, Explosion
from objects.dinosaur import Direction

from .object_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler
from data_containers import objects as obj_container, game_data


class TriceratopsHandler(ObjectHandler, DinosaurHandler):
    REACTIONS_SEE: dict[Obstacle.Type, str] = {
        Obstacle.Type.CACTUS: None,
        Obstacle.Type.THORNS: 'start_biting',
        Obstacle.Type.STONE: None,
        Obstacle.Type.TREE: None,
        Obstacle.Type.FERN: 'start_biting',
        Obstacle.Type.SKELETON: None,
    }

    REACTIONS_TOUCH: dict[Obstacle.Type, str] = {
        Obstacle.Type.CACTUS: 'destroy_obstacle',
        Obstacle.Type.THORNS: 'eat_obstacle',
        Obstacle.Type.STONE: 'destroy_obstacle',
        Obstacle.Type.TREE: 'destroy_obstacle',
        Obstacle.Type.FERN: 'eat_obstacle',
        Obstacle.Type.SKELETON: 'destroy_obstacle',
    }

    @classmethod
    def update(cls, obj: Triceratops) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        update_delta: int = obj.update_delta

        # Process invincibility (resist to bites only)
        obj.invincibility = max(0, obj.invincibility - obj.update_delta)

        # Stop biting
        if (
            obj.state == obj.State.BITING
            and obj.curr_frame_head >= obj.TOTAL_FRAMES_HEAD - 1
            and get_ticks() - obj.last_frame_change_head >= obj.calc_anim_interval(obj.ANIM_INTERVAL_HEAD)
        ):
            obj.curr_frame_head = 0
            obj.last_frame_change_head = get_ticks()
            obj.state = obj.State.RUNNING

        # Accelerate
        accel_x = obj.VEL_X_MAX / obj.VEL_X_MAX_IN / 1000 * update_delta
        obj.vel_x = min(
            obj.vel_x + (accel_x if obj.hitbox.bottom >= obj_container.get_ground().touch_level else 0),
            obj.VEL_X_MAX
        )

        # React to environment
        for other_obj in obj_container.visible().values():
            # Skip oneself, different layer, beyond reach
            if other_obj.id == obj.id or obj.LAYER != obj.LAYER.MAIN or not obj.fov_around.overlaps(other_obj.rect):
                continue

            # NPC
            if isinstance(other_obj, Dinosaur):
                cls.react_to_npc(obj, other_obj)

            # Obstacles
            elif isinstance(other_obj, Obstacle):
                cls.react_to_obstacles(obj, other_obj)
            # TODO Reaction to touching the poop

        # TODO Poop if belly's full
        # ...

        obj.last_update = get_ticks()

    @classmethod
    def react_to_npc(cls, triceratops: Triceratops, other_dino: Dinosaur) -> None:
        # Cache
        triceratops_hitbox_head = triceratops.hitbox_head
        triceratops_hitbox_body = triceratops.hitbox_body
        other_dino_hitbox = other_dino.hitbox

        # Head/horns collision (attack)
        if triceratops_hitbox_head.overlaps(other_dino_hitbox):
            if getattr(other_dino, 'invincibility', 0) > 0:
                return

            other_dino.health -= 1
            cls.bounce(
                other_dino,
                triceratops,
                triceratops_hitbox_head.center_x >= other_dino_hitbox.center_x
            )

            if isinstance(other_dino, TRexNew):
                other_dino.invincibility = other_dino.INVINCIBILITY_DURATION
                return

            if other_dino.health <= 0:
                explosion = Explosion(
                    spawn=Obstacle.make_skeleton(other_dino) if other_dino.weight >= game_data.HEAVY_DINOSAUR_WEIGHT else None,
                ).instead_of(other_dino)

                obj_container.queue_delete(other_dino)
                obj_container.add(explosion)

            # TODO Check humans
            # ...

            return

        # Body collision - bounce
        elif triceratops_hitbox_body.overlaps(other_dino.hitbox):
            if getattr(other_dino, 'invincibility', 0) > 0:
                return

            cls.bounce(
                other_dino,
                triceratops,
                triceratops_hitbox_body.center_x >= other_dino_hitbox.center_x
            )

    @classmethod
    def start_biting(cls, dinosaur: Triceratops, obstacle: Obstacle) -> None:
        if dinosaur.state != dinosaur.State.BITING:
            dinosaur.state = Triceratops.State.BITING

    @classmethod
    def eat_obstacle(cls, dinosaur: Triceratops, obstacle: Obstacle) -> None:
        if (
            dinosaur.state == dinosaur.State.BITING
            and dinosaur.curr_frame_head >= dinosaur.TOTAL_FRAMES_HEAD - 1
            and dinosaur.hitbox_bite.overlaps(obstacle.rect)
        ):
            dinosaur.heal(1)

            obj_container.queue_delete(obstacle)

    @classmethod
    def destroy_obstacle(cls, triceratops: Triceratops, obstacle: Obstacle) -> None:
        explosion = Explosion()
        explosion.rect.center_x = obstacle.rect.center_x
        explosion.rect.center_y = obstacle.rect.center_y

        obj_container.queue_delete(obstacle)
        obj_container.queue_add(explosion)

        triceratops.vel_x /= 2

        if triceratops.hitbox.bottom >= obj_container.get_ground().touch_level:
            triceratops.vel_y = triceratops.JUMP_ACCEL


    @classmethod
    def delete_if_passed_camera(cls, obj: Triceratops) -> bool:
        if obj.rect.left >= obj_container.get_camera().rect.right:
            obj_container.queue_delete(obj)
            return True

        return False