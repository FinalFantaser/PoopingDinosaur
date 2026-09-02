from .object import Object


class ObjectWithPhysics(Object):
    """
    Generic class for objects with physical properties
    """

    __slots__ = Object.__slots__ + (
        "vel_x",
        "vel_y",
    )

    HANDLER_NAME: str = "SkeletonHandler"
    WEIGHT_FACTOR: float = 1.0

    def __init__(
            self,
            id: str,
            pos: tuple[int | float, int | float] = (0, 0),
            size: tuple[int | float, int | float] = (0, 0),
            texture_name: str | None = None,
            total_frames: int = 1,
            anim_interval: int = 0,
    ) -> None:
        super().__init__(id, pos, size, texture_name, total_frames, anim_interval)
        self.vel_x: float = 0
        self.vel_y: float = 0