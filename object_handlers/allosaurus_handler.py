from pygame.time import get_ticks
from objects import Object, Ground, Obstacle, Poo, Skeleton, Dinosaur, TRexNew, Allosaurus, FlattenedObject
from .object_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler
from data_containers import objects as obj_container, game_data


class AllosaurusHandler(ObjectHandler, DinosaurHandler):
    REACTION_OBJECTS_SEE: dict[type[Object], str] = {
        Skeleton: "skeleton_see",
        Poo: "poo_see",
        TRexNew: "trex_see",
    }

    REACTION_OBJECTS_TOUCH: dict[type[Object], str] = {
        Skeleton: "skeleton_touch",
        TRexNew: "trex_touch",
    }

    @classmethod
    def update(cls, obj: Allosaurus) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)
        cls.accelerate(obj)
        obj.stop_biting()

        # React to environment
        for other_obj in obj_container.visible().values():
            if cls.skip_irrelevant_object(obj, other_obj, (not obj.fov_around.overlaps(other_obj.rect),)):
                continue

            cls.react_to_objects(obj, other_obj)

        obj.last_update = get_ticks()

    @classmethod
    def jump_over_object(cls, dinosaur: Dinosaur, obstacle: Object) -> None:
        if dinosaur.state == Dinosaur.State.RUNNING or dinosaur.state == Dinosaur.State.BITING:
            dinosaur_rect = dinosaur.hitbox
            obstacle_rect = getattr(obstacle, "hitbox", obstacle.rect)

            if dinosaur.fov_ahead.overlaps(
                    obstacle.rect) and dinosaur_rect.bottom >= obj_container.get_ground().touch_level:
                obstacle_edge: float = obstacle_rect.right if dinosaur.direction.value[0] < 0 else obstacle_rect.left
                dinosaur_edge: float = dinosaur_rect.left if dinosaur.direction.value[0] < 0 else dinosaur_rect.right

                if abs(obstacle_edge - dinosaur_edge) <= dinosaur_rect.width * 0.5:
                    dinosaur.vel_y = dinosaur.JUMP_ACCEL

    @classmethod
    def start_biting(cls, allosaurus: Allosaurus, object: TRexNew|Obstacle) -> None:
        if allosaurus.state != allosaurus.State.BITING:
            allosaurus.start_biting()


    @classmethod
    def attack(cls, allosaurus: Allosaurus, trex: TRexNew) -> None:
        if trex.invincibility > 0:
            return

        if allosaurus.is_biting():
            if allosaurus.hitbox_bite.overlaps(trex.hitbox):
                trex.health -= 1
                trex.invincibility = TRexNew.INVINCIBILITY_DURATION

                trex.vel_x = trex.VEL_X_MIN * 0.5 * allosaurus.direction.value[0]
                trex.vel_y = trex.jump_impulse * 0.8

    @classmethod
    def fern_touch(cls, dinosaur: Allosaurus, fern: Obstacle) -> None:
        if dinosaur.is_biting() and dinosaur.hitbox_bite.overlaps(fern.rect):
            obj_container.queue_delete(fern)
            return

        # Slow down
        dinosaur.vel_x = min(abs(dinosaur.vel_x) / 2, dinosaur.VEL_X_MIN / 2) * dinosaur.direction.value[0]

    @classmethod
    def skeleton_touch(cls, dinosaur: Allosaurus, skeleton: Skeleton) -> None:
        cls.bounce(dinosaur, skeleton, skeleton.rect.center_x > dinosaur.hitbox.center_x)

    @classmethod
    def trex_touch(cls, dinosaur: Allosaurus, trex: TRexNew) -> None:
        cls.attack(dinosaur, trex)

    @classmethod
    def fern_see(cls, dinosaur: Allosaurus, fern: Obstacle) -> None:
        cls.start_biting(dinosaur, fern)

    @classmethod
    def skeleton_see(cls, dinosaur: Dinosaur, skeleton: Skeleton) -> None:
        cls.jump_over_object(dinosaur, skeleton)

    @classmethod
    def trex_see(cls, dinosaur: Allosaurus, trex: TRexNew) -> None:
        cls.start_biting(dinosaur, trex)

    @classmethod
    def poo_see(cls, dinosaur: Allosaurus, poo: Poo) -> None:
        cls.jump_over_object(dinosaur, poo)