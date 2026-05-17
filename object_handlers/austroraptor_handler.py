import pygame.time
from objects import Object, Austroraptor, TRex, Ground
from data_containers import objects as obj_container, game_data
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

        # Gravity
        if obj.rect.bottom < ground.touch_level:
            fall_accel: float = game_data.GRAVITY_PIXELS * obj.WEIGHT_FACTOR
            obj.vel_y += fall_accel / 1000 * update_delta

        obj.y += obj.vel_y / 1000 * update_delta
        if obj.rect.bottom >= ground.touch_level:
            obj.vel_y = 0.0
            obj.rect.bottom = ground.touch_level

        # Reacting to other dinosaurs
        for other_obj in obj_container.visible().values():
            if obj.id == other_obj.id:
                continue

            if not isinstance(other_obj, cls._HUNTERS):
                continue

            if not obj.trigger_area.overlaps(other_obj.rect):
                continue

            # Get startled
            if obj.state == Austroraptor.State.IDLE:
                obj.state = Austroraptor.State.STARTLED
                if obj.rect.bottom >= ground.touch_level:
                    obj.vel_y = obj.JUMP_ACCEL * 0.5

        obj.last_update = pygame.time.get_ticks()