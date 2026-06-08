import pygame.time
from objects import Dinosaur, Pterodactyl
from data_containers import objects as obj_container
from .object_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler


class PterodactylHandler(ObjectHandler, DinosaurHandler):
    @classmethod
    def update(cls, obj: Pterodactyl) -> None:
        if cls.delete_if_passed_camera(obj):
            obj_container.queue_delete(obj)
            return

        cls.physics(obj)
        obj.y = max(obj.y, Pterodactyl.MAX_ALTITUDE)

        if obj.state == obj.State.DEAD:
            return

        if obj.vel_y >= obj.VEL_Y_MAX_ALLOWED or obj.rect.bottom >= obj_container.get_ground().touch_level:
            obj.flap_wings()

        obj.last_update = pygame.time.get_ticks()