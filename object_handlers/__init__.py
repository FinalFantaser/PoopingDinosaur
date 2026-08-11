# System objects
from .object_handler import ObjectHandler
from .camera_handler import CameraHandler

# Dinosaurs
from .dinosaur_handler import DinosaurHandler
from .trex_handler import TRexHandler
from .austroraptor_handler import AustroraptorHandler
from .velociraptor_handler import VelociraptorHandler
from .pterodactyl_handler import PterodactylHandler
from .triceratops_handler import TriceratopsHandler

# Environment
from .obstacle_handler import ObstacleHandler
from .poo_handler import PooHandler
from .explosion_handler import ExplosionHandler

# GUI
from .gui.health_meter_handler import HealthMeterHandler
from .gui.poo_handler import PooMeterHandler
from .gui.pause_menu_handler import PauseMenuHandler


object_handlers: dict[str, type[ObjectHandler]] = {
    handler_class.__name__: handler_class for handler_class in ObjectHandler.__subclasses__()
}