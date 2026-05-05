from objects import Allosaurus, GuiPooMeter
from object_handlers.object_handler import ObjectHandler
from data_containers import objects as obj_container


class GuiPooMeterHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: GuiPooMeter) -> None:
        allosaurus: Allosaurus = obj_container.get_player()
        obj.value = allosaurus.poos