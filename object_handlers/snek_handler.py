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
        TRexNew.__name__: "trex_see",
    }

    REACTION_OBJECTS_TOUCH: dict[str, str] = {
        Skeleton.__name__: None,
        Geyser.__name__: "geyser_touch",
        TRexNew.__name__: "trex_touch",
    }

    @classmethod
    def update(cls, obj: Snek):
        last_ticks = get_ticks()
        time_delta = obj.update_delta

        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        # Slow down
        if obj.vel_x != 0:
            decel_x = obj.VEL_X_MIN / 1000 / obj.SLOWDOWN_TIME * time_delta

            if obj.vel_x > 0:
                obj.vel_x = max(0.0, obj.vel_x - decel_x)
            else:
                obj.vel_x = min(0.0, obj.vel_x + decel_x)

        # Behaviour
        if obj.state == obj.State.IDLE:
            cls.process_idle_state(obj, last_ticks)
        elif obj.state == obj.State.BITING:
            cls.process_biting_state(obj)

        obj.last_update = last_ticks

    @classmethod
    def process_idle_state(cls, snek: Snek, ticks: int) -> None:
        # Turn
        if ticks - snek.last_turn_at >= snek.TURN_INTERVAL:
            snek.direction = snek.direction.opposite()

        # Reacting to TRex
        trex: TRexNew|None = obj_container.get(TRexNew.ID)
        if trex is not None and snek.fov_ahead.overlaps(trex.rect):
            snek.curr_frame = 0
            snek.state = snek.State.BITING
            snek.vel_x = snek.VEL_X_MIN * snek.direction.value[0]
            snek.vel_y = snek.JUMP_ACCEL

    @classmethod
    def process_biting_state(cls, snek: Snek) -> None:
        # Touching the T-Rex
        trex: TRexNew | None = obj_container.get(TRexNew.ID)
        if trex is not None and snek.hitbox.overlaps(trex.hitbox) and trex.invincibility > 0:
            trex.invincibility = trex.INVINCIBILITY_DURATION
            cls.bounce_back(trex, snek)

        # Touching the ground and getting apathetic
        if snek.hitbox.bottom >= obj_container.get_ground().touch_level:
            snek.state = snek.State.CORNERED

    @classmethod
    def trex_see(cls, snek: Snek, trex: TRexNew) -> None:
        pass

    @classmethod
    def trex_touch(cls, snek: Snek, trex: TRexNew) -> None:
        pass

    @classmethod
    def geyser_touch(cls, dinosaur: Snek, geyser: Geyser) -> None:
        if geyser.erupting:
            dinosaur.die()