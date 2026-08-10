import pygame.time

from objects import Object, Obstacle, Dinosaur, Triceratops
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
        pass

    @classmethod
    def coll_human(cls, triceratops: Triceratops, human) -> None:
        pass

    @classmethod
    def coll_obstacle(cls, triceratops: Triceratops, obstacle: Obstacle) -> None:
        pass