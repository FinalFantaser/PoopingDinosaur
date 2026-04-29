from objects import Camera, Ground, Allosaurus
from data_containers import objects as obj_container
from object_handlers.object_handler import ObjectHandler


class CameraHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Camera) -> None:
        ground: Ground = obj_container.get(Ground.ID)
        allosaurus: Allosaurus = obj_container.get(Allosaurus.ID)

        obj.rect.center_x = allosaurus.rect.center_x

        if obj.rect.left < ground.rect.left:
            obj.rect.left = ground.rect.left
        elif obj.rect.right > ground.rect.right:
            obj.rect.right = ground.rect.right
