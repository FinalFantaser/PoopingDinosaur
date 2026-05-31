from pygame import Rect as PygameRect
import core.video
from objects.object import Rect, Object


class PooMeter(Object):
    __slots__ = *Object.__slots__, "value"

    LAYER: Object.Layer = Object.Layer.GUI
    HANDLER_NAME: str | None = "PooMeterHandler"
    ID: str = "gui_poo_meter"
    SIZE_POO: tuple[float, float] = 16, 16
    SIZE_METER: tuple[float, float] = SIZE_POO[0] * 5, 16
    POS: tuple[float, float] = SIZE_POO[0]/2, core.video.get_screen_rect().bottom - SIZE_METER[1] * 1.5
    TEXTURE_NAME: str = "poo.png"
    POO_DRAW_RECT: PygameRect = PygameRect((0, 0), SIZE_POO)

    def __init__(self, value: int) -> None:
        super().__init__(
            id=self.ID,
            pos=self.POS,
            size=self.SIZE_METER,
            texture_name=self.TEXTURE_NAME
        )

        self.value: int = value


    def draw(self, viewpoint: Rect) -> None:
        if self.value < 1:
            return

        draw_x: float = self.POS[0]
        for _ in range(self.value):
            core.video.texture_blit(
                self.TEXTURE_NAME,
                (draw_x, self.POS[1]),
                self.POO_DRAW_RECT
            )
            draw_x += self.SIZE_POO[0] * 1.5