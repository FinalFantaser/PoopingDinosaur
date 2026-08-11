import pygame.time

from objects import Obstacle, Dinosaur, TRex, Triceratops, Velociraptor
from objects.dinosaur import Direction

from .object_handler import ObjectHandler
from data_containers import objects as obj_container


class TriceratopsHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Triceratops) -> None:
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
            obj_container.queue_delete(other_dino)
            # TODO Create explosion, then skeleton

        # Body collision - bounce
        direction: Direction = triceratops.direction.opposite() if triceratops.center_x - other_dino.center_x < 0 else triceratops.direction
        other_dino.vel_x = other_dino.vel_x * 1.5 * direction.value
        other_dino.vel_y = min(Velociraptor.JUMP_ACCEL, -other_dino.WEIGHT * 0.7)


    @classmethod
    def coll_human(cls, triceratops: Triceratops, human) -> None:
        pass

    @classmethod
    def coll_obstacle(cls, triceratops: Triceratops, obstacle: Obstacle) -> None:
        pass