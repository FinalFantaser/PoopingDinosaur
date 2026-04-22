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

def delete(obj: Object, throw: bool = False) -> None:
    pass