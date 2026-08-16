class GameData:
    """
    Attributes:
        HEAVY_DINOSAUR_WEIGHT: minimum weight (kg) of a dinosaur considered to be heavy.
    """

    GRAVITY: float = 9.8
    PIXELS_PER_METER: float = 100.0
    GRAVITY_PIXELS: float = GRAVITY * PIXELS_PER_METER

    HEAVY_DINOSAUR_WEIGHT: int = 1500

    def __init__(self):
        self.score: int = 0
        self.pause: bool = False
        self.quit: bool = False


game_data: GameData = GameData()