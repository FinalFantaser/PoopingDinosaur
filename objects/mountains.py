from .tiled_background import Layer, TiledBackground


class Mountains(TiledBackground):
    LAYER: Layer = Layer.BACKGROUND_2
    ID: str = 'mountains'
    TEXTURE_NAME: str = 'bg_mountains.png'
    BLOCK_VAR_RANGE: int = 3