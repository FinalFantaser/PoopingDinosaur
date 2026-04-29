import core.video
from objects.object import Object, Rect


class Camera(Object):
    ID: str = 'camera'
    VISIBLE: bool = False
    HANDLER_NAME: str|None = 'CameraHandler'

    def __init__(self, pos: tuple[int|float, int|float]):
        super().__init__(
            id=self.ID,
            pos=pos,
            size=core.video.get_screen_rect().size
        )

    def within_viewpoint(self, other_obj: Object) -> bool:
        return self.rect.overlaps(other_obj.rect)

    @property
    def viewpoint(self) -> Rect:
        return self.rect

    @property
    def left(self) -> float:
        return self.rect.left

    @left.setter
    def left(self, new_left: float) -> None:
        self.rect.left = new_left

    @property
    def right(self) -> float:
        return self.rect.right

    @right.setter
    def right(self, new_right: float) -> None:
        self.rect.right = new_right