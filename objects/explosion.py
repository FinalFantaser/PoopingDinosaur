from .object import Object


class Explosion(Object):
    __slots__ = *Object.__slots__, "spawn"

    """
    Explosion object. Mostly for decoration but can spawn other objects after fading if necessary.
    
    Attributes:
         spawn: An object to be spawned in place of the explosion as it fades.
         total: Total amount of the explosions created (used for id).
    """

    HANDLER_NAME = "ExplosionHandler"
    ID_STUB: str = "explosion_%d"
    SIZE: tuple[float, float] = 32, 32
    TEXTURE_NAME: str = "explosion.png"
    ANIM_INTERVAL: int = 100
    TOTAL_FRAMES = 3

    total: int = 0

    def __init__(self, pos: tuple[int | float, int | float] = (0, 0), spawn: Object|None = None):
        self.total += 1

        super().__init__(
            id=self.ID_STUB % self.total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL
        )

        self.spawn: Object|None = spawn
