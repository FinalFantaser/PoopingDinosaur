from pygame.time import get_ticks
from typing import Callable
from objects import Object, Direction, Dinosaur, Ground, Obstacle
from data_containers import objects as obj_container

class DinosaurHandler:
    """
    General class/interface to handle repeating dinosaur behavior
    and define individual reactions to dinosaurs and obstacles.
    """

    REACTIONS_TOUCH: dict[Obstacle.Type, str] = {
        Obstacle.Type.CACTUS: 'cactus_touch',
        Obstacle.Type.THORNS: 'thorns_touch',
        Obstacle.Type.STONE: 'stone_touch',
        Obstacle.Type.TREE: 'tree_touch',
        Obstacle.Type.FERN: 'fern_touch',
        Obstacle.Type.SKELETON: 'skeleton_touch',
    }

    REACTIONS_SEE: dict[Obstacle.Type, str] = {
        Obstacle.Type.CACTUS: 'cactus_see',
        Obstacle.Type.THORNS: 'thorns_see',
        Obstacle.Type.STONE: 'stone_see',
        Obstacle.Type.TREE: 'tree_see',
        Obstacle.Type.FERN: 'fern_see',
        Obstacle.Type.SKELETON: 'skeleton_see',
    }

    EDIBLES: tuple[type[Object], ...] = ()

    @classmethod
    def react_to_hunter(cls, prey: Dinosaur, hunter: Dinosaur) -> None:
        """
        React to a hunter by switching states and directions
        :param prey: Reacting dinosaur.
        :param hunter: Hunter dinosaur to react to.
        """
        # Do nothing if the hunter is dead
        if isinstance(prey, Dinosaur) and prey.state == prey.State.DEAD:
            return

        ground: Ground = obj_container.get_ground()

        # If idle, get startled and jump
        if prey.state == prey.State.IDLE:
            prey.state = prey.State.STARTLED

            if prey.rect.bottom >= ground.touch_level:
                prey.vel_y = prey.JUMP_ACCEL / 4

        # If startled and landed after the jump, run away from the hunter
        elif prey.state == prey.State.STARTLED and prey.rect.bottom >= ground.touch_level:
            prey.state = prey.State.RUNNING
            prey.direction = Direction.RIGHT if prey.rect.center_x >= hunter.rect.center_x else Direction.LEFT

        #  If running and got behind the hunter, run to opposite direction
        elif prey.state == prey.State.RUNNING:
            old_dir: Direction = prey.direction
            prey.direction = Direction.RIGHT if prey.rect.center_x >= hunter.rect.center_x else Direction.LEFT
            if prey.direction != old_dir:
                prey.vel_x = abs(prey.vel_x / 2) * prey.direction.value[0]

    @classmethod
    def react_to_obstacles(cls, dinosaur: Dinosaur, obstacle: Obstacle) -> None:
        """
        Wrapper assembling all methods handling touching and reacting to obstacles in dinosaur's FOV.
        :param dinosaur: Reacting dinosaur.
        :param obstacle: Obstacle to react to.
        """
        for hitbox, method_list in (
            (dinosaur.hitbox, cls.REACTIONS_TOUCH), # If touched
            (dinosaur.fov_ahead, cls.REACTIONS_SEE), # If seen
        ):
            if hitbox.overlaps(obstacle.rect):
                method_name: str = method_list[obstacle.ob_type]
                if method_name is None:
                    break

                method: Callable | None = getattr(cls, method_name)

                if method is None:
                    raise NotImplementedError(f"{cls.__name__}.{method_name}")

                method(dinosaur, obstacle)

                break

    @classmethod
    def jump_over_obstacle(cls, dinosaur: Dinosaur, obstacle: Obstacle) -> None:
        """
        Attempt to jump over an obstacle when running. Considered as a general behaviour.
        :param dinosaur: Jumping dinosaur.
        :param obstacle: Obstacle to jump over.
        """
        if dinosaur.state == Dinosaur.State.RUNNING:
            if dinosaur.fov_ahead.overlaps(obstacle.rect) and dinosaur.rect.bottom >= obj_container.get_ground().touch_level:
                obstacle_edge: float = obstacle.rect.right if dinosaur.direction.value[0] < 0 else obstacle.rect.left
                dinosaur_edge: float = dinosaur.rect.left if dinosaur.direction.value[0] < 0 else dinosaur.rect.right

                if abs(obstacle_edge - dinosaur_edge) <= dinosaur.width * 1.5:
                    dinosaur.vel_y = dinosaur.JUMP_ACCEL

    @classmethod
    def bounce(
            cls,
            dinosaur: Dinosaur,
            obstacle: Obstacle|Dinosaur,
            opposite_dir: bool,
            override_vel_x: float|None = None,
            override_jump: float|None = None,
    ):
        """Bounce in a specifed direction of current movement with quarter of current horizontal velocity."""
        vel_x = override_vel_x if override_vel_x is not None else dinosaur.vel_x * 0.25
        vel_y = override_jump if override_jump is not None else dinosaur.JUMP_ACCEL / 2

        cur_vel_modifier = 1 if vel_x >= 0 else -1
        limited_vel = min(dinosaur.VEL_X_MAX * 1.65, abs(vel_x)) * cur_vel_modifier

        dinosaur.vel_x = limited_vel * (-1 if opposite_dir else 1)
        dinosaur.vel_y = vel_y

    @classmethod
    def bounce_back(
            cls, dinosaur: Dinosaur,
            obstacle: Obstacle|Dinosaur,
            override_vel_x: float | None = None,
            override_jump: float | None = None,
    ) -> None:
        cls.bounce(dinosaur, obstacle, True, override_vel_x, override_jump)

    @classmethod
    def cactus_touch(cls, dinosaur: Dinosaur, cactus: Obstacle) -> None:
        """
        React to touching cactus.
        :param dinosaur: Reacting dinosaur.
        :param cactus: Cactus to react to.
        """
        # Switch to DEAD and throw the dinosaur back
        dinosaur.state = Dinosaur.State.DEAD
        dinosaur.vel_x = dinosaur.VEL_X_MIN / 4 * dinosaur.direction.opposite().value[0]
        dinosaur.vel_y = dinosaur.JUMP_ACCEL / 4

    @classmethod
    def thorns_touch(cls, dinosaur: Dinosaur, thorns: Obstacle) -> None:
        """
        React to touching thorns.
        :param dinosaur: Reacting dinosaur.
        :param thorns: Thorns to react to.
        """
        # Slow down
        dinosaur.vel_x = min(dinosaur.vel_x/2, dinosaur.VEL_X_MIN/2) * dinosaur.direction.value[0]

    @classmethod
    def stone_touch(cls, dinosaur: Dinosaur, stone: Obstacle) -> None:
        """
        React to touching stone.
        :param dinosaur: Reacting dinosaur.
        :param stone: Stone to react to.
        """
        # Stumble and go forward with slight acceleration
        ground: Ground = obj_container.get_ground()

        if dinosaur.rect.bottom >= ground.touch_level:
            if dinosaur.rect.bottom >= ground.touch_level:
                dinosaur.vel_y = dinosaur.JUMP_ACCEL / 25 - dinosaur.vel_x/3
            else:
                dinosaur.vel_y = dinosaur.JUMP_ACCEL / 30 - dinosaur.vel_x/3

            dinosaur.vel_x = min(dinosaur.vel_x * 2.5, dinosaur.VEL_X_MAX * 1.25)

    @classmethod
    def tree_touch(cls, dinosaur: Dinosaur, tree: Obstacle) -> None:
        """
        React to touching tree.
        :param dinosaur: Reacting dinosaur.
        :param tree: Tree to react to.
        """
        cls.bounce_back(dinosaur, tree)

    @classmethod
    def fern_touch(cls, dinosaur: Dinosaur, fern: Obstacle) -> None:
        """
        React to touching ferns.
        :param dinosaur: Reacting dinosaur.
        :param fern: Thorns to react to.
        """
        # Slow down
        dinosaur.vel_x = min(dinosaur.vel_x / 2, dinosaur.VEL_X_MIN / 2) * dinosaur.direction.value[0]

    @classmethod
    def skeleton_touch(cls, dinosaur: Dinosaur, skeleton: Obstacle) -> None:
        """
        React to touching a skeleton.
        :param dinosaur: Reacting dinosaur.
        :param skeleton: Thorns to react to.
        """
        cls.bounce_back(dinosaur, skeleton)

    @classmethod
    def cactus_see(cls, dinosaur: Dinosaur, cactus: Obstacle) -> None:
        cls.jump_over_obstacle(dinosaur, cactus)

    @classmethod
    def thorns_see(cls, dinosaur: Dinosaur, thorns: Obstacle) -> None:
        cls.jump_over_obstacle(dinosaur, thorns)

    @classmethod
    def stone_see(cls, dinosaur: Dinosaur, stone: Obstacle) -> None:
        cls.jump_over_obstacle(dinosaur, stone)

    @classmethod
    def tree_see(cls, dinosaur: Dinosaur, tree: Obstacle) -> None:
        cls.jump_over_obstacle(dinosaur, tree)

    @classmethod
    def fern_see(cls, dinosaur: Dinosaur, fern: Obstacle) -> None:
        cls.jump_over_obstacle(dinosaur, fern)

    @classmethod
    def skeleton_see(cls, dinosaur: Dinosaur, skeleton: Obstacle) -> None:
        pass