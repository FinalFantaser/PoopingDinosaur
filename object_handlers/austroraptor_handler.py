import pygame.time
from objects import Rect, Direction, Object, Dinosaur, Austroraptor, TRex, TRexNew, Ground, Obstacle, Poo
from data_containers import objects as obj_container

from .object_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler

class AustroraptorHandler(ObjectHandler, DinosaurHandler):
    _HUNTERS: tuple[type[Object], ...] = TRex, TRexNew

    @classmethod
    def update(cls, obj: Austroraptor) -> None:
        update_delta: int = obj.update_delta

        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        # Reacting to other dinosaurs
        for other_obj in obj_container.visible().values():
            if obj.id == other_obj.id or isinstance(other_obj, Ground):
                continue

            if not obj.fov_around.overlaps(other_obj.rect):
                continue

            if isinstance(other_obj, cls._HUNTERS):
                cls.react_to_hunter(obj, other_obj)
            elif isinstance(other_obj, Obstacle):
                cls.react_to_obstacles(obj, other_obj)

        # Accelerate to maximum speed when running
        if obj.state == Austroraptor.State.RUNNING:
            accel_x: float = Austroraptor.VEL_X_MAX / Austroraptor.VEL_X_MAX_IN / 1000 * update_delta
            obj.vel_x = min(obj.vel_x + accel_x, Austroraptor.VEL_X_MAX)
        # Slow down if dead
        if obj.state == Austroraptor.State.DEAD:
            obj.vel_x = 0.0

        obj.last_update = pygame.time.get_ticks()