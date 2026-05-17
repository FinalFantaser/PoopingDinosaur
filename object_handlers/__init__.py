from .object_handler import ObjectHandler
from .camera_handler import CameraHandler
from .trex_handler import TRexHandler
from .austroraptor_handler import AustroraptorHandler
from .poo_handler import PooHandler

from .gui.health_meter_handler import HealthMeterHandler
from .gui.poo_handler import PooMeterHandler
from .gui.pause_menu_handler import PauseMenuHandler


object_handlers: dict[str, type[ObjectHandler]] = {
    handler_class.__name__: handler_class for handler_class in ObjectHandler.__subclasses__()
}