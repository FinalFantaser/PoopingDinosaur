from objects import TRex, PooMeter
from object_handlers.object_handler import ObjectHandler
from data_containers import objects as obj_container


class PooMeterHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: PooMeter) -> None:
        allosaurus: TRex = obj_container.get_player()
        obj.value = allosaurus.poos