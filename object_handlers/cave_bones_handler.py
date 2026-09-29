import core.video
from objects import Rect, CaveBones
from data_containers import objects as obj_container
from .object_handler import ObjectHandler


class CaveBonesHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: CaveBones):
        if cls.delete_if_passed_camera(obj):
            return

    @classmethod
    def delete_if_passed_camera(cls, obj: CaveBones):
        parallax_camera = obj_container.get_camera().rect.with_parallax(CaveBones.PARALLAX_FACTOR)

        if obj.rect.right < parallax_camera.x:
            obj_container.queue_delete(obj)