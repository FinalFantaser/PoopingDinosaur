from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Zombiesaurus
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data
from .obstacle_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler

class ZombiesaurusHandler(ObjectHandler, DinosaurHandler):
    @classmethod
    def update(cls, obj: Zombiesaurus):
        time_delta = obj.update_delta

        if cls.delete_if_passed_camera(obj):
            return

        if obj.state == obj.State.IDLE:
            obj.emerge_progress = max(obj.emerge_progress - time_delta, 0)
            if obj.emerge_progress <= 0:
                obj.state = obj.State.RUNNING
        elif obj.state == obj.State.RUNNING or obj.state == obj.state.BITING:
            cls.physics(obj)
            cls.accelerate(obj)

            # React to environment
            # ...

        obj.last_update = get_ticks()