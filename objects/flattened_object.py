import core.video
from typing import Self
from pygame import Color
from pygame.time import get_ticks
from .rect import Rect
from .object_with_physics import Object, ObjectWithPhysics


class FlattenedObject(ObjectWithPhysics):
    """
    A flat line used to show that the object was flattened. Disappears after some time.
    """

    __slots__ = ObjectWithPhysics.__slots__ + (
        "created_at",
    )

    HANDLER_NAME: str = "FlattenedObjectHandler"
    ID_STUB: str = "flattened_%s"
    WEIGHT_FACTOR: float = 0.8
    LIFETIME: int = 1000
    THICKNESS: int = 1
    COLOR: Color = Color(0, 0, 0)

    def __init__(self, id: str, width: float|int, pos: tuple[float|int, float|int] = (0, 0)) -> None:
        self.created_at: int = get_ticks()
        super().__init__(
            id=id,
            pos=pos,
            size=(width, self.THICKNESS)
        )

    def draw(self, viewpoint: Rect):
        rect: Rect = self.rect

        start = int(rect.left - viewpoint.x), int(rect.bottom - viewpoint.y)
        end = int(rect.right - viewpoint.x), int(rect.bottom - viewpoint.y)

        core.video.draw_line(start, end, self.COLOR, self.THICKNESS)

    @classmethod
    def instead_of(cls, other_obj: Object) -> Self:
        return cls(
            id=cls.ID_STUB % other_obj.id,
            width=other_obj.rect.width,
            pos=(
                other_obj.rect.left,
                other_obj.rect.bottom - cls.THICKNESS,
            )
        )