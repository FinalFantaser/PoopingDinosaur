import pygame.time

from objects import Obstacle, Dinosaur, TRex, Triceratops, Velociraptor, Explosion
from objects.dinosaur import Direction

from .object_handler import ObjectHandler
from data_containers import objects as obj_container


class TriceratopsHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Triceratops) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        # Accelerate
        if obj.vel_x < obj.VEL_X_MAX:
            accel = float(obj.update_delta) * obj.VEL_X_MAX / obj.VEL_X_MAX_IN
            obj.vel_x = min(obj.VEL_X_MAX, obj.vel_x + accel)


        # Handle collisions:
        camera = obj_container.get_camera()
        for other_obj in obj_container.visible().values():
            # Skip oneself, different layer, not touched ones
            if other_obj.id == obj.id or obj.LAYER != obj.LAYER.MAIN or not obj.hitbox.overlaps(other_obj.rect):
                continue

            # Dinosaurs
            if isinstance(other_obj, Dinosaur):
                cls.coll_dinosaur(obj, other_obj)

            # Humans
            # ...

            # Obstacles
            elif isinstance(other_obj, Obstacle):
                cls.coll_obstacle(obj, other_obj)

        obj.last_update = pygame.time.get_ticks()

    @classmethod
    def coll_dinosaur(cls, triceratops: Triceratops, other_dino: Dinosaur) -> None:
        # Head/horns collision (attack)
        if other_dino.hitbox.overlaps(triceratops.hitbox_head):
            if isinstance(other_dino, TRex) and other_dino.invincibility < 1:
                other_dino.health = max(0, other_dino.health - 1)
                other_dino.invincibility = 3000

                other_dino.vel_x_modifier = other_dino.VEL_X_MODIFIER * 2.5

            elif isinstance(other_dino, Dinosaur):
                skeleton = Obstacle(
                    Obstacle.Type.SKELETON,
                    (
                        other_dino.x,
                        other_dino.y - Obstacle.SIZES[Obstacle.Type.SKELETON][1]/2,
                    )
                )

                explosion = Explosion(other_dino.pos, skeleton)

                obj_container.queue_delete(other_dino)
                obj_container.queue_add(explosion)

            return

        # Body collision - bounce
        direction: Direction = triceratops.direction.opposite() if triceratops.rect.center_x - other_dino.rect.center_x < 0 else triceratops.direction
        other_dino.vel_x = other_dino.vel_x * 1.5 * direction.value[0]
        other_dino.vel_y = min(Velociraptor.JUMP_ACCEL, -other_dino.WEIGHT * 0.7)


    @classmethod
    def coll_human(cls, triceratops: Triceratops, human) -> None:
        pass

    @classmethod
    def coll_obstacle(cls, triceratops: Triceratops, obstacle: Obstacle) -> None:
        explosion = Explosion(obstacle.pos)

        obj_container.queue_delete(obstacle)
        obj_container.queue_add(explosion)