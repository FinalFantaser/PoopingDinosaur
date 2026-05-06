from objects import Allosaurus, HealthMeter
from object_handlers.object_handler import ObjectHandler
from data_containers import objects as obj_container

class HealthMeterHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: HealthMeter) -> None:
        allosaurus: Allosaurus = obj_container.get_player()
        obj.value = allosaurus.health