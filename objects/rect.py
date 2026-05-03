class Rect:
    __slots__ = ("x", "y", "width", "height")

    def __init__(self, x: int|float, y: int|float, width: int|float, height: int|float) -> None:
        self.x: float = float(x)
        self.y: float = float(y)
        self.width: float = float(width)
        self.height: float = float(height)

    def overlaps(self, other_rect: 'Rect') -> bool:
        return (
                self.left < other_rect.right
                and self.right > other_rect.left
                and self.top < other_rect.bottom
                and self.bottom > other_rect.top
        )

    @property
    def size(self) -> tuple[float, float]:
        return self.width, self.height

    @size.setter
    def size(self, size: tuple[float, float]) -> None:
        self.width, self.height = float(size[0]), float(size[1])

    @property
    def left(self) -> float:
        return self.x

    @left.setter
    def left(self, new_left: float|int) -> None:
        self.x = float(new_left)

    @property
    def right(self) -> float:
        return self.x + self.width

    @right.setter
    def right(self, new_right: float|int) -> None:
        self.x = float(new_right) - self.width

    @property
    def top(self) -> float:
        return self.y

    @top.setter
    def top(self, new_top: float|int) -> None:
        self.y = float(new_top)

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @bottom.setter
    def bottom(self, new_bottom: float|int) -> None:
        self.y = float(new_bottom) - self.height

    @property
    def top_left(self) -> tuple[float, float]:
        return self.left, self.top

    @top_left.setter
    def top_left(self, new_topleft: tuple[float|int, float|int]) -> None:
        self.x, self.y = float(new_topleft[0]), float(new_topleft[1])

    @property
    def top_right(self) -> tuple[float, float]:
        return self.right, self.top

    @top_right.setter
    def top_right(self, new_topright: tuple[float|int, float|int]) -> None:
        self.top, self.right = float(new_topright[0]), float(new_topright[1])

    @property
    def bottom_left(self) -> tuple[float, float]:
        return self.left, self.bottom

    @bottom_left.setter
    def bottom_left(self, new_bottom_left: tuple[float|int, float|int]) -> None:
        self.left, self.bottom = float(new_bottom_left[0]), float(new_bottom_left[1])

    @property
    def bottom_right(self) -> tuple[float, float]:
        return self.right, self.bottom

    @bottom_right.setter
    def bottom_right(self, new_bottom_right: tuple[float|int, float|int]) -> None:
        self.right, self.bottom = float(new_bottom_right[0]), float(new_bottom_right[1])

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @center_x.setter
    def center_x(self, new_x: float|int) -> None:
        self.x = float(new_x) - self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2

    @center_y.setter
    def center_y(self, new_y: float|int) -> None:
        self.y = float(new_y) - self.height / 2

    @property
    def center(self) -> tuple[float, float]:
        return self.center_x, self.center_y

    @center.setter
    def center(self, new_center: tuple[float|int, float|int]) -> None:
        self.center_x, self.center_y = float(new_center[0]), float(new_center[1])

    @property
    def pos(self) -> tuple[float, float]:
        return self.top_left

    @pos.setter
    def pos(self, new_pos: tuple[float|int, float|int]) -> None:
        self.top_left = new_pos

    def to_tuple(self) -> tuple[float, float, float, float]:
        return self.x, self.y, self.width, self.height