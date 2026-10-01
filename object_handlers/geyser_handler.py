from pygame.time import get_ticks
from objects import Geyser
from .object_handler import ObjectHandler

class GeyserHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Geyser) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        curr_ticks = get_ticks()

        if obj.erupting:
            if curr_ticks - obj.started_erupting_at >= obj.ERUPTION_DURATION:
                obj.stop_erupting()
        else:
            if curr_ticks - obj.stopped_erupting_at >= obj.ERUPTION_INTERVAL:
                obj.start_erupting()

        obj.last_update = curr_ticks