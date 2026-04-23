from pygame import Surface
import pygame.time
import core.paths
import core.video
from objects.rect import Rect

class Object:
    VISIBLE: bool = True
    HANDLER_NAME: str|None = None

    def __init__(
            self,
            id: str,
            pos: tuple[int|float, int|float] = (0, 0),
            size: tuple[int|float, int|float] = (0, 0),
            texture_name: str|None = None,
            total_frames: int = 0,
            anim_interval: int = 0,
    ) -> None:
        self.id: str = id
        self.rect: Rect = Rect(pos[0], pos[1], size[0], size[1])
        self.texture_name: str|None = texture_name
        self.total_frames: int = total_frames
        self.anim_interval: int = anim_interval
        self.last_frame_change: int = pygame.time.get_ticks()

        if self.texture_name is not None:
            core.video.texture_load(core.paths.TEXTURES / self.texture_name)

    def draw(self) -> None:
        pass

    @property
    def x(self) -> float:
        return self.rect.x

    @x.setter
    def x(self, value: int|float) -> None:
        self.rect.x = float(value)

    @property
    def y(self) -> float:
        return self.rect.y

    @y.setter
    def y(self, value: float|int) -> None:
        self.rect.y = float(value)

    @property
    def width(self) -> float:
        return self.rect.width

    @width.setter
    def width(self, value: float|int) -> None:
        self.rect.width = float(value)

    @property
    def height(self) -> float:
        return self.rect.height

    @height.setter
    def height(self, value: float|int) -> None:
        self.rect.height = float(value)

    @property
    def size(self) -> tuple[float, float]:
        return self.rect.size

    @size.setter
    def size(self, value: tuple[float|int, float|int]) -> None:
        self.rect.size = (float(value[0]), float(value[1]))

    @property
    def pos(self) -> tuple[int|float, int|float]:
        return self.rect.pos

    @pos.setter
    def pos(self, value: tuple[int|float, int|float]) -> None:
        self.rect.pos = value

    @property
    def texture(self) -> Surface|None:
        return core.video.texture_get(self.texture_name)