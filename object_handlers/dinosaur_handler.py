from objects import Dinosaur

class DinosaurHandler:
    """
    General class/interface to handle repeating dinosaur behavior
    and define individual reactions to dinosaurs and obstacles.
    """

    @classmethod
    def react_to_hunter(cls, obj: Dinosaur, hunter: Dinosaur) -> None:
        pass