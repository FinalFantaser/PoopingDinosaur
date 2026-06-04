import pygame.time
from objects import Rect, Direction, Object, Dinosaur, Austroraptor, TRex, Ground, Obstacle, Poo
from data_containers import objects as obj_container

from .object_handler import ObjectHandler

class AustroraptorHandler(ObjectHandler):
    _HUNTERS: tuple[type[Object], ...] = (
        TRex,
    )

    @classmethod
    def update(cls, obj: Austroraptor) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        update_delta: int = obj.update_delta
        ground: Ground = obj_container.get_ground()

        # Gravity and horizontal movement
        cls.physics(obj)

        # Reacting to other dinosaurs
        for other_obj in obj_container.visible().values():
            if obj.id == other_obj.id or isinstance(other_obj, Ground):
                continue

            # Get startled and attempt to escape a hunter
            if isinstance(other_obj, cls._HUNTERS):
                # If idle, get startled and jump
                if obj.state == Austroraptor.State.IDLE and obj.fov_around.overlaps(other_obj.rect):
                    obj.state = Austroraptor.State.STARTLED
                    if obj.rect.bottom >= ground.touch_level:
                        obj.vel_y = obj.JUMP_ACCEL * 0.5

                # If running and got behind the hunter, run to opposite direction
                elif obj.state == Austroraptor.State.RUNNING:
                    new_direction: Direction = (Direction.RIGHT if obj.rect.center_x >= other_obj.rect.center_x else Direction.LEFT)
                    if obj.direction != new_direction and obj.rect.bottom >= ground.touch_level:
                        obj.direction = new_direction
                        obj.vel_x = max(obj.vel_x/2, obj.VEL_X_MIN)

                # Run away as soon as landed
                elif obj.state == Austroraptor.State.STARTLED and obj.rect.bottom >= ground.touch_level:
                    obj.state = Austroraptor.State.RUNNING
                    obj.direction = Direction.RIGHT if obj.rect.center_x >= other_obj.rect.center_x else Direction.LEFT

            elif isinstance(other_obj, Obstacle|Poo):
                # Attempt to jump over an obstacle when running
                if obj.state == Austroraptor.State.RUNNING:
                    vicinity: Rect = Rect(
                        obj.rect.left - obj.rect.width * 3 if obj.direction == Direction.LEFT else obj.rect.right,
                        obj.rect.y,
                        *obj.rect.size
                    )

                    if vicinity.overlaps(other_obj.rect) and obj.rect.bottom >= ground.touch_level:
                        obj.vel_y = obj.JUMP_ACCEL

                if obj.rect.overlaps(other_obj.rect) and obj.state != Austroraptor.State.DEAD:
                    obj.vel_y = obj.JUMP_ACCEL
                    obj.direction = Direction.LEFT if obj.rect.center_x < other_obj.rect.center_x else Direction.RIGHT
                    obj.state = Austroraptor.State.DEAD

        # Accelerate to maximum speed when running
        if obj.state == Austroraptor.State.RUNNING:
            accel_x: float = Austroraptor.VEL_X_MAX / Austroraptor.VEL_X_MAX_IN / 1000 * update_delta
            obj.vel_x = min(obj.vel_x + accel_x, Austroraptor.VEL_X_MAX)
        # Slow down if dead
        if obj.state == Austroraptor.State.DEAD:
            obj.vel_x = 0.0

        obj.last_update = pygame.time.get_ticks()