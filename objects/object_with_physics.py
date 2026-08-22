from .object import Object


class ObjectWithPhysics(Object):
    """
    Generic class for objects with physical properties
    """

    __slots__ = Object.__slots__ + (
        "vel_x",
        "vel_y",
    )

    WEIGHT_FACTOR: float = 1.0