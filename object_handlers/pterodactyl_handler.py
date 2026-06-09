import pygame.time
from objects import Direction, Ground, TRex, Dinosaur, Pterodactyl, Obstacle
from data_containers import objects as obj_container, game_data
from .object_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler


class PterodactylHandler(ObjectHandler, DinosaurHandler):
    @classmethod
    def update(cls, obj: Pterodactyl) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        if cls.delete_if_passed_camera(obj):
            obj_container.queue_delete(obj)
            return

        cls.physics(obj)

        if obj.state == obj.State.DEAD:
            return

        if obj.vel_y >= obj.VEL_Y_MAX_ALLOWED or obj.rect.bottom >= obj_container.get_ground().touch_level:
            obj.flap_wings()

        # Reacting to dinosaurs
        for other_obj in obj_container.visible().values():
            if other_obj.id == obj.id or isinstance(other_obj, (Pterodactyl, Ground, Obstacle)):
                continue

            if isinstance(other_obj, (Dinosaur, TRex)):
                cls.react_to_hunter(prey=obj, hunter=other_obj)

        # Handling states
        if obj.state == obj.State.IDLE:
            if abs(obj.rect.center_x - obj.last_turn_pos) >= obj.MAX_ROAM_DISTANCE:
                obj.direction = obj.direction.opposite()
                obj.vel_x = 0.0
                obj.last_turn_pos = obj.rect.center_x
        elif obj.state == obj.State.RUNNING:
            if abs(obj.rect.center_x - obj.last_turn_pos) >= obj.MAX_ROAM_DISTANCE:
                obj.altitude_limit = None

        obj.last_update = pygame.time.get_ticks()

    @classmethod
    def physics(cls, obj: Pterodactyl) -> None:
        update_delta: int = obj.update_delta
        ground: Ground = obj_container.get_ground()

        # Gravity
        if obj.rect.bottom < ground.touch_level:
            fall_accel: float = game_data.GRAVITY_PIXELS * obj.WEIGHT_FACTOR
            obj.vel_y += fall_accel / 1000 * update_delta

        obj.y += obj.vel_y / 1000 * update_delta
        if obj.rect.bottom >= ground.touch_level:
            obj.vel_y = 0.0
            obj.rect.bottom = ground.touch_level

        # Vertical flight
        if obj.altitude_limit is not None:
            obj.y = max(obj.y, obj.altitude_limit)

        # Horizontal movement
        accel_x = obj.vel_x/1000 * update_delta
        obj.x += accel_x

    @classmethod
    def react_to_hunter(cls, prey: Pterodactyl, hunter: TRex|Dinosaur) -> None:
        if isinstance(hunter, Dinosaur) and hunter.state == hunter.State.DEAD:
            return

        if prey.state == prey.State.IDLE:
            if prey.fov_around.overlaps(hunter.rect):
                cls.change_direction(prey, hunter)
                prey.vel_x = prey.VEL_X_MIN / 3
                prey.state = prey.State.RUNNING
                prey.last_turn_pos = prey.x
                prey.gear = 2
        elif prey.state == prey.State.RUNNING:
            if prey.fov_around.overlaps(hunter.rect):
                cls.change_direction(prey, hunter)

    @classmethod
    def change_direction(cls, prey: Pterodactyl, hunter: Dinosaur) -> None:
        old_direction: Direction = prey.direction
        prey.direction = Direction.RIGHT if prey.rect.center_x > hunter.rect.center_x else Direction.LEFT
        if prey.direction != old_direction:
            prey.vel_x = 0.0