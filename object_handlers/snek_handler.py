from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Obstacle, Geyser, Skeleton, Snek, TRexNew, Dinosaur
from .object_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler
from data_containers import objects as obj_container, game_data


class SnekHandler(ObjectHandler, DinosaurHandler):
    REACTIONS_OBSTACLE_TOUCH: dict[Obstacle.Type, str] = {
        Obstacle.Type.CACTUS: None,
        Obstacle.Type.THORNS: None,
        Obstacle.Type.STONE: None,
        Obstacle.Type.TREE: None,
        Obstacle.Type.FERN: None,
        Obstacle.Type.OIL: None,
    }

    REACTIONS_OBSTACLE_SEE: dict[Obstacle.Type, str] = {
        Obstacle.Type.CACTUS: None,
        Obstacle.Type.THORNS: None,
        Obstacle.Type.STONE: None,
        Obstacle.Type.TREE: None,
        Obstacle.Type.FERN: None,
        Obstacle.Type.OIL: None,
    }

    REACTION_OBJECTS_SEE: dict[str, str] = {
        Skeleton.__name__: None,
        Geyser.__name__: None,
    }

    REACTION_OBJECTS_TOUCH: dict[str, str] = {
        Skeleton.__name__: None,
        Geyser.__name__: "geyser_touch",
    }

    @classmethod
    def update(cls, obj: Snek):
        time_delta = obj.update_delta

        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        if obj.state == obj.State.IDLE:
            pass
        elif obj.state == obj.State.BITING:
            pass

        if obj.state != obj.State.DEAD:
            pass

        obj.last_update = get_ticks()

    @classmethod
    def process_idle_state(cls, snek: Snek) -> None:
        pass

    @classmethod
    def process_biting_state(cls, snek: Snek) -> None:
        pass

    @classmethod
    def react_to_trex(cls, snek: Snek, trex: TRexNew) -> None:
        pass

    @classmethod
    def geyser_touch(cls, dinosaur: Snek, geyser: Geyser) -> None:
        if geyser.erupting:
            dinosaur.die()