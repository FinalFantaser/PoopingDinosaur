class GameData:
    GRAVITY: float = 9.8
    PIXELS_PER_METER: float = 100.0
    GRAVITY_PIXELS: float = GRAVITY * PIXELS_PER_METER

    def __init__(self):
        self.score: int = 0
        self.pause: bool = False


game_data: GameData = GameData()