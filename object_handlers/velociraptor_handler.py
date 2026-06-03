import pygame.time
from objects import Direction, Ground, Camera, TRex, Dinosaur, Austroraptor, Velociraptor, Obstacle
from data_containers import objects as obj_container
from .object_handler import ObjectHandler


class VelociraptorHandler(ObjectHandler):
    _HUNTERS: tuple[type[TRex|Dinosaur], ...] = TRex, Austroraptor

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

            if isinstance(other_obj, (Ground, Velociraptor)):
                continue

            if not obj.fov.overlaps(other_obj.rect):
                continue

            if isinstance(other_obj, cls._HUNTERS) and isinstance(obj, Dinosaur) and obj.state != obj.State.DEAD:
                cls.react_to_dinosaur(obj, other_obj)
            else:
                cls.react_to_obstacle(obj, other_obj)

        # Accelerate to maximum speed when running
        if obj.state == obj.State.RUNNING:
            accel_x: float = obj.VEL_X_MAX / obj.VEL_X_MAX_IN / 1000 * update_delta
            obj.vel_x = min(obj.vel_x + accel_x, Austroraptor.VEL_X_MAX)
        # Slow down if dead
        if obj.state == Austroraptor.State.DEAD:
            obj.vel_x = 0.0

        obj.last_update = pygame.time.get_ticks()


    @classmethod
    def react_to_dinosaur(cls, obj: Velociraptor, other_obj: TRex|Dinosaur) -> None:
        ground: Ground = obj_container.get_ground()

        # If velociraptor is idle, get startled and jump
        if obj.state == obj.State.IDLE:
            obj.state = obj.State.STARTLED

            if obj.rect.bottom >= ground.touch_level:
                obj.vel_y = obj.JUMP_ACCEL / 2

        # If startled and landed after the jump, run away from the hunter
        elif obj.state == obj.State.STARTLED and obj.rect.bottom >= ground.touch_level:
            obj.state = obj.State.RUNNING
            obj.direction = Direction.RIGHT if obj.rect.center_x >= other_obj.rect.center_x else Direction.LEFT

        #  If running and got behind the hunter, run to opposite direction
        elif obj.state == obj.State.RUNNING:
            old_dir: Direction = obj.direction
            obj.direction = Direction.RIGHT if obj.rect.center_x >= other_obj.rect.center_x else Direction.LEFT
            if obj.direction != old_dir:
                obj.vel_x = abs(obj.vel_x/2) * obj.direction.value[0]



    @classmethod
    def react_to_obstacle(cls, obj: Velociraptor, obstacle: Obstacle) -> None:
        # If touched:
        # ...

        # If obstacle is in the way, switch to CORNERED state
        pass