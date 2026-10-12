from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Obstacle, Ground, Camera, Zephyrosaurus, TRexNew
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

        cls.physics(obj)
        cls.clear_unexistent_touches(obj)

        if obj.state == obj.State.RUNNING:
            # Burrow ...
            # ...
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

        obj.last_update = get_ticks()

