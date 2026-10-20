from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Obstacle, Poo, Explosion, Dinosaur, Snek, TRexNewCave, Zombiesaurus, Zephyrosaurus
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data
from .obstacle_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler

class ZombiesaurusHandler(ObjectHandler, DinosaurHandler):
    REACTIONS_OBSTACLE_TOUCH: dict[Obstacle.Type, str] = {}
    REACTIONS_OBSTACLE_SEE: dict[Obstacle.Type, str] = {}
    REACTION_OBJECTS_SEE: dict[str, str] = {
        Snek.__name__: "start_biting",
        TRexNewCave.__name__: "start_biting",
        Zephyrosaurus.__name__: "start_biting",
    }

    REACTION_OBJECTS_TOUCH: dict[str, str] = {
        Snek.__name__: "attack",
        TRexNewCave.__name__: "attack",
        Zephyrosaurus.__name__: "attack",
    }

    @classmethod
    def update(cls, obj: Zombiesaurus):
        time_delta = obj.update_delta

        if cls.delete_if_passed_camera(obj):
            return

        if obj.state == obj.State.IDLE:
            obj.emerge_progress = max(obj.emerge_progress - time_delta, 0)
            if obj.emerge_progress <= 0:
                obj.state = obj.State.RUNNING
        elif obj.state == obj.State.RUNNING or obj.state == obj.state.BITING:
            cls.physics(obj)
            cls.accelerate(obj)
            obj.stop_biting()

            for other_obj in obj_container.main_layer().values():
                if cls.skip_irrelevant_object(
                        obj,
                        other_obj,
                        (not isinstance(other_obj, (Zephyrosaurus, Snek, TRexNewCave)),)
                ):
                    continue

                cls.react_to_objects(obj, other_obj)

        obj.last_update = get_ticks()

    @classmethod
    def start_biting(cls, zombie: Zombiesaurus, prey: Dinosaur) -> None:
        if zombie.state != zombie.State.BITING:
            zombie.start_biting()

    @classmethod
    def attack(cls, zombie: Zombiesaurus, prey: Dinosaur) -> None:
        if prey.invincibility > 0:
            return

        if zombie.is_biting():
            if zombie.hitbox_bite.overlaps(prey.hitbox):
                if isinstance(prey, TRexNewCave):
                    prey.health -= 1
                    prey.invincibility = TRexNewCave.INVINCIBILITY_DURATION

                    prey.vel_x = prey.VEL_X_MIN * 0.5 * zombie.direction.value[0]
                    prey.vel_y = prey.jump_impulse * 0.8
                elif isinstance(prey, (Snek, Zephyrosaurus)):
                    obj_container.queue_delete(prey)

    @classmethod
    def delete_if_passed_camera(cls, obj: Zombiesaurus) -> bool:
        viewpoint = obj_container.get_camera()

        if obj.direction == Direction.LEFT:
            return obj.rect.right <= viewpoint.left - viewpoint.width * 0.5
        else:
            return obj.rect.left >= viewpoint.right + viewpoint.width * 0.5