from random import randint
from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Obstacle, Ground, Camera, Zephyrosaurus, TRexNew, Dinosaur
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data
from .dinosaur_handler import DinosaurHandler

class ZephyrosaurusHandler(ObjectHandler, DinosaurHandler):
    REACTION_OBJECTS_SEE: dict[str, str] = {
        **DinosaurHandler.REACTION_OBJECTS_SEE,
        TRexNew.__name__: "react_to_hunter"
    }

    @classmethod
    def update(cls, obj: Zephyrosaurus):
        if cls.delete_if_passed_camera(obj):
            return

        if obj.burrow_progress >= obj.BURROW_TIME:
            obj_container.queue_delete(obj)
            return

        last_ticks = get_ticks()

        cls.physics(obj)
        cls.clear_unexistent_touches(obj)

        if obj.state == obj.State.IDLE or  obj.state == obj.State.STARTLED:
            for other_obj in obj_container.visible().values():
                if cls.skip_irrelevant_object(
                        obj,
                        other_obj,
                        (
                            not obj.fov_around.overlaps(other_obj.rect),
                            not isinstance(other_obj, TRexNew)
                        )
                ):
                    continue
                cls.react_to_objects(obj, other_obj)

        elif obj.state == obj.State.RUNNING:
            if last_ticks >= obj.burrow_time:
                obj.state = obj.State.CORNERED
                obj.vel_x = 0
            else:
                cls.accelerate(obj)

                # React to environment
                for other_obj in obj_container.visible().values():
                    if cls.skip_irrelevant_object(
                            obj,
                            other_obj,
                            (not obj.fov_around.overlaps(other_obj.rect),)
                    ):
                        continue

                    cls.react_to_objects(obj, other_obj)
        elif obj.state == obj.State.CORNERED:
            obj.burrow_progress = min(obj.burrow_progress + obj.update_delta, obj.BURROW_TIME)
        elif obj.state == obj.State.DEAD:
            obj.vel_x = 0

        obj.last_update = get_ticks()

    @classmethod
    def react_to_hunter(cls, prey: Zephyrosaurus, hunter: Dinosaur) -> None:
        prev_state = prey.state
        super().react_to_hunter(prey, hunter)

        if prey.state == prey.State.RUNNING and prey.state != prev_state:
            prey.burrow_time = get_ticks() + randint(prey.BURROW_TIME_RANGE[0], prey.BURROW_TIME_RANGE[1])