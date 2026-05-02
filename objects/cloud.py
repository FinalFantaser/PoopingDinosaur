import core.paths
import core.video
from objects.object import Object, Rect


class Cloud(Object):
    ID_STUB: str = "cloud_%d"
    TEXTURE_NAME: str = "cloud.png"
    SIZE: tuple[float, float] = (32.0, 16.0)
    LAYER: int = -2
    
    _total: int = 0
    
    def __init__(self, pos: tuple[int|float, int|float]) -> None:
        self._total += 1
        
        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE
        )
        
        if not core.video.texture_has(self.TEXTURE_NAME):
            core.video.texture_load(core.paths.TEXTURES / self.TEXTURE_NAME, self.TEXTURE_NAME)
    
    def draw(self, viewpoint: Rect) -> None:
        if not self.rect.overlaps(viewpoint):
            return
        
        # Adding a parallax effect
        draw_pos: tuple[float, float] = (
            self.x - viewpoint.x - self.LAYER,
            self.y - viewpoint.y
        )
            
        core.video.texture_blit(self.TEXTURE_NAME, draw_pos)
