from objects import Allosaurus, GuiHealthMeter, Object
from object_handlers.object_handler import ObjectHandler
from data_containers import objects as obj_container

class GuiHealthMeterHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: GuiHealthMeter) -> None:
        allosaurus: Allosaurus = obj_container.get(Allosaurus.ID, True)
        obj.value = allosaurus.health