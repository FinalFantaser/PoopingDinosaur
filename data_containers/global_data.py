_score: int = 0
_done: bool = False


def get_score() -> int:
    return _score


def set_score(score: int) -> int:
    global _score
    _score = score
    return _score


def get_done() -> bool:
    return _done


def set_done(value: bool) -> bool:
    global _done
    _done = value
    return _done