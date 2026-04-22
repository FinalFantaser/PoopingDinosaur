from objects import Object

_all: dict[str, Object] = {}

_idx_visible: list[str] = []
_idx_hidden: list[str] = []
_idx_with_handlers: list[str] = []

def clear() -> None:
    _all.clear()
    _idx_visible.clear()
    _idx_hidden.clear()

def add(obj: Object) -> None:
    _all[obj.id] = obj

    if obj.VISIBLE:
        _idx_visible.append(obj.id)
    else:
        _idx_hidden.append(obj.id)

def delete(obj: Object, throw: bool = False) -> Object|None:
    if obj.id not in _all:
        if throw:
            raise KeyError(f"Object with id {obj.id} was not found.")
        else:
            return None

    if obj.VISIBLE:
        _idx_visible.remove(obj.id)
    else:
        _idx_hidden.remove(obj.id)

    return _all.pop(obj.id)