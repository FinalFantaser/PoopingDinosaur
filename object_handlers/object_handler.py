from data_containers import objects as obj_container
from objects import *


class ObjectHandler:
    @classmethod
    def update(cls, obj: Object) -> None:
        pass

    @classmethod
    def read_input(cls, obj: Object) -> None:
        pass

    @classmethod
    def delete_if_passed_camera(cls, obj: Object) -> bool:
        if obj.rect.right < obj_container.get_camera().rect.left:
            obj_container.queue_delete(obj)
            return True

        return False
