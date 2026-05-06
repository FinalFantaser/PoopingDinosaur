from .object_handler import ObjectHandler
from .camera_handler import CameraHandler
from .allosaurus_handler import AllosaurusHandler
from .poo_handler import PooHandler

from object_handlers.gui.health_meter_handler import HealthMeterHandler
from object_handlers.gui.poo_handler import PooMeterHandler


object_handlers: dict[str, type[ObjectHandler]] = {
    handler_class.__name__: handler_class for handler_class in ObjectHandler.__subclasses__()
}