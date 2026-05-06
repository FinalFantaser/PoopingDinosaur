import core.video
from objects.object import Layer, Object, Rect


class HealthMeter(Object):
    __slots__ = *Object.__slots__, "value"

    LAYER: Layer = Layer.GUI
    HANDLER_NAME: str | None = "HealthMeterHandler"

    ID: str = "gui_health_meter"
    POS: tuple[float, float] = 8, 8
    SIZE_METER: tuple[float, float] = 52, 8
    SIZE_HEART: tuple[float, float] = 8, 8
    TEXTURE_NAME: str = "heart.png"

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
            )
            draw_x += self.SIZE_HEART[0] * 1.5