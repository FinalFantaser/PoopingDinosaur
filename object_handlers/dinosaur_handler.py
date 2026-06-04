from copy import copy
from objects import Rect, Direction, Dinosaur, Ground, Obstacle
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
    }

    REACTIONS_SEE: dict[Obstacle.Type, str] = {
        Obstacle.Type.CACTUS: 'cactus_see',
        Obstacle.Type.THORNS: 'thorns_see',
        Obstacle.Type.STONE: 'stone_see',
        Obstacle.Type.TREE: 'tree_see',
    }

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

        # If velociraptor is idle, get startled and jump
        if prey.state == prey.State.IDLE:
            prey.state = prey.State.STARTLED

            if prey.rect.bottom >= ground.touch_level:
                prey.vel_y = prey.JUMP_ACCEL / 2

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
        # If touched
        if dinosaur.hitbox.overlaps(obstacle.rect):
            method_name: str = cls.REACTIONS_TOUCH[obstacle.ob_type]
            getattr(cls, method_name)(dinosaur, obstacle)
            return

        # If seen
        if dinosaur.hitbox.overlaps(obstacle.rect):
            method_name: str = cls.REACTIONS_SEE[obstacle.ob_type]
            getattr(cls, method_name)(dinosaur, obstacle)
            return


    @classmethod
    def cactus_touch(cls, dinosaur: Dinosaur, cactus: Obstacle) -> None:
        """
        React to touching cactus.
        :param dinosaur: Reacting dinosaur.
        :param cactus: Cactus to react to.
        """
        # Swtich to DEAD and throw the dinosaur back
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
        dinosaur.vel_x = min(dinosaur.vel_x/2, dinosaur.VEL_X_MIN/2)

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
        # Bounce back
        dinosaur.vel_x = dinosaur.VEL_X_MIN / 4 * dinosaur.direction.opposite().value[0]
        dinosaur.vel_y = dinosaur.JUMP_ACCEL / 2

    @classmethod
    def jump_over_obstacle(cls, dinosaur: Dinosaur, obstacle: Obstacle) -> None:
        """
        Attempt to jump over an obstacle when running. Considered as a general behaviour.
        :param dinosaur: Jumping dinosaur.
        :param obstacle: Obstacle to jump over.
        """
        if dinosaur.state == Dinosaur.State.RUNNING:
            if dinosaur.fov_ahead.overlaps(obstacle.rect) and dinosaur.rect.bottom >= obj_container.get_ground().touch_level:
                dinosaur.vel_y = dinosaur.JUMP_ACCEL

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