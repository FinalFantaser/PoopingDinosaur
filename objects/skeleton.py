from pygame.time import get_ticks
from typing import Self
import core.video
from .rect import Rect
from .object import Object
from .object_with_physics import ObjectWithPhysics


class Skeleton(ObjectWithPhysics):
    __slots__ = *Object.__slots__, "created_at"

    HANDLER_NAME = "SkeletonHandler"
    ID_STUB: str = "%s_skeleton"
    TEXTURE_NAME: None = "skeleton.png"
    SIZE: tuple[float, float] = 32, 9
    TOTAL_FRAMES: int = 1
    ANIM_INTERVAL: int = 0
    WEIGHT_FACTOR: float = 0.17
    INVINCIBILITY_DURATION: int = 1000

    def __init__(self, id: str, pos: tuple[int | float, int | float] = (0, 0)) -> None:
        super().__init__(id, pos, self.SIZE, self.TEXTURE_NAME, self.TOTAL_FRAMES, self.ANIM_INTERVAL)
        self.created_at: int = get_ticks()

    def draw(self, viewpoint: Rect) -> None:
        core.video.texture_blit(
            self.texture_name,
            (self.x - viewpoint.x, self.y - viewpoint.y),
        )

    @classmethod
    def instead_of(cls, obj: Object) -> Self:
        skeleton = cls(
            cls.ID_STUB % obj.id,
            (0, 0)
        )

        obj_rect = getattr(obj, "hitbox", "rect")
        skeleton.rect.center = obj_rect.center_x, obj_rect.center_y - obj_rect.height

        return skeleton

    def is_invincible(self) -> bool:
        return get_ticks() - self.created_at < self.INVINCIBILITY_DURATION