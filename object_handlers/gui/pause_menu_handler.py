import pygame.time
import core.input
from objects import PauseMenu
from data_containers import objects as obj_container, game_data
from object_handlers.object_handler import ObjectHandler


class PauseMenuHandler(ObjectHandler):
    @classmethod
    def read_input(cls, obj: PauseMenu) -> None:
        if obj.update_delta >= obj.INPUT_READ_INTERVAL:
            if core.input.held("up"):
                obj.prev()
            elif core.input.held("down"):
                obj.next()

            obj.last_update = pygame.time.get_ticks()

        if core.input.pressed("confirm") or core.input.pressed("poop"):
            obj_container.queue_delete(obj)
            obj_container.reset_updated_at()
        elif core.input.pressed("back") or core.input.pressed("pause"):
            obj_container.queue_delete(obj)
            obj_container.reset_updated_at()