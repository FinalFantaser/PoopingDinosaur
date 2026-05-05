import core.paths
import core.video
from objects.object import Layer, Object, Rect


class Cloud(Object):
    __slots__ = *Object.__slots__, 'last_draw_pos'
    ID_STUB: str = "cloud_%d"
    TEXTURE_NAME: str = "cloud.png"
    SIZE: tuple[float, float] = (32.0, 16.0)
    LAYER: Layer = Layer.BACKGROUND_2
    PARALLAX_FACTOR: float = 0.6
    _total: int = 0
    
    def __init__(self, pos: tuple[int|float, int|float]) -> None:
        Cloud._total += 1
        
        super().__init__(
            id=self.ID_STUB % Cloud._total,
            pos=pos,
            size=self.SIZE
        )

        self.last_draw_pos: tuple[float, float] = 0, 0
        
        if not core.video.texture_has(self.TEXTURE_NAME):
            core.video.texture_load(core.paths.TEXTURES / self.TEXTURE_NAME, self.TEXTURE_NAME)
    
    def draw(self, viewpoint: Rect) -> None:
        viewpoint_parallax: Rect = Rect(
            x=viewpoint.x * self.PARALLAX_FACTOR,
            y=viewpoint.y * self.PARALLAX_FACTOR,
            width=viewpoint.width,
            height=viewpoint.height
        )

        if not self.rect.overlaps(viewpoint_parallax):
            return

        draw_pos: tuple[float, float] = (
            self.x - viewpoint_parallax.x,
            self.y - viewpoint_parallax.y
        )
            
        core.video.texture_blit(self.TEXTURE_NAME, draw_pos)