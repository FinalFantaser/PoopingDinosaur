from pygame.time import get_ticks
from objects.skeleton import Skeleton
from .object_handler import ObjectHandler


class SkeletonHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Skeleton) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        obj.last_update = get_ticks()