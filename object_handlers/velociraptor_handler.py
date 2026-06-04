import pygame.time
from objects import Direction, Ground, Camera, TRex, Dinosaur, Austroraptor, Velociraptor, Obstacle
from data_containers import objects as obj_container
from .object_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler


class VelociraptorHandler(ObjectHandler, DinosaurHandler):
    _HUNTERS: tuple[type[TRex|Dinosaur], ...] = TRex, #Austroraptor

    @classmethod
    def update(cls, obj: Velociraptor) -> None:
        update_delta: int = obj.update_delta

        cls.delete_if_passed_camera(obj)
        cls.physics(obj)

        if obj.state == obj.State.DEAD:
            return

        # Reacting to environment
        for other_obj in obj_container.visible().values():
            if obj.id == other_obj.id:
                continue

            if not obj.fov_around.overlaps(other_obj.rect):
                continue

            if isinstance(other_obj, cls._HUNTERS):
                cls.react_to_hunter(obj, other_obj)
            elif isinstance(other_obj, Obstacle):
                cls.react_to_obstacles(obj, other_obj)

        # Accelerate to maximum speed when running
        if obj.state == obj.State.RUNNING:
            accel_x: float = obj.VEL_X_MAX / obj.VEL_X_MAX_IN / 1000 * update_delta
            obj.vel_x = min(obj.vel_x + accel_x, Austroraptor.VEL_X_MAX)
        # Slow down if dead
        if obj.state == Austroraptor.State.DEAD:
            obj.vel_x = 0.0

        obj.last_update = pygame.time.get_ticks()

    @classmethod
    def cactus_see(cls, dinosaur: Dinosaur, cactus: Obstacle) -> None:
        cls.get_cornered(dinosaur, cactus)

    @classmethod
    def thorns_touch(cls, dinosaur: Dinosaur, thorns: Obstacle) -> None:
        obj_container.queue_delete(dinosaur)

    @classmethod
    def thorns_see(cls, dinosaur: Dinosaur, thorns: Obstacle) -> None:
        pass

    @classmethod
    def get_cornered(cls, dinosaur: Dinosaur, obstacle: Obstacle) -> None:
        if dinosaur.state == dinosaur.State.RUNNING:
            obstacle_edge: float = obstacle.rect.right if dinosaur.direction.value[0] < 0 else obstacle.rect.left
            dinosaur_edge: float = dinosaur.rect.left if dinosaur.direction.value[0] < 0 else dinosaur.rect.right

            if abs(obstacle_edge - dinosaur_edge) <= dinosaur.width * 1.5:
                dinosaur.vel_x = 0

                if dinosaur.rect.bottom >= obj_container.get_ground().touch_level:
                    dinosaur.vel_y = dinosaur.JUMP_ACCEL

    @classmethod
    def stone_see(cls, dinosaur: Dinosaur, stone: Obstacle) -> None:
        cls.get_cornered(dinosaur, stone)