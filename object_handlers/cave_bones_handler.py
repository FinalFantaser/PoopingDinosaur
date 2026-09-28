import core.video
from objects import CaveBones
from data_containers import objects as obj_container
from .object_handler import ObjectHandler


class CaveBonesHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: CaveBones):
        if cls.delete_if_passed_camera(obj):
            return

    @classmethod
    def delete_if_passed_camera(cls, obj: CaveBones):
        if obj_container.get_camera().x - obj.rect.right >= core.video.get_screen_rect().width/2:
            obj_container.queue_delete(obj)