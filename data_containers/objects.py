from enum import Enum
from typing import Iterable, Self
from objects import Object, Layer, Camera, TRexNew, TRexNewCave, Ground, Dinosaur


class _TaskType(int, Enum):
    ADD = 0
    DELETE = 1


class _Task:
    __slots__ = ("type", "subject", "throw")
    def __init__(self, type: _TaskType, subject: Object | str, throw: bool = False) -> None:
        self.type: _TaskType = type
        self.subject: Object|str = subject
        self.throw: bool = throw


class Filter:
    def __init__(
            self,
            obj_type: type[Object]|Iterable[type[Object]]|None = None,
            layer: Layer|None = None,
            visible: bool|None = None,
            with_handler: bool|None = None,
            id: str|None = None,
            limit: int = 1,
            return_type: type[dict|set|tuple|list] = type[dict],
    ):
        # Validation
        if limit < 1:
            raise ValueError(f"Invalid filter limit: {limit} (must be > 0)")

        self.obj_type: type[Object]|Iterable[type[Object]]|None = obj_type
        self.layer: Layer | None = layer
        self.visible: bool|None = visible
        self.with_handler: bool|None = with_handler
        self.id: str|None = id
        self.limit: int = limit
        self.return_type: type[dict|set|tuple|list] = return_type

    def by_type(self, obj_type: type[Object]|Iterable[type[Object]]|None) -> Self:
        self.obj_type = obj_type
        return self

    def by_layer(self, layer: Layer | None) -> Self:
        self.layer = layer
        return self

    def by_visible(self, visible: bool | None) -> Self:
        self.visible = visible
        return self

    def by_with_handler(self, with_handler: bool | None) -> Self:
        self.with_handler = with_handler
        return self

    def by_id(self, id: str | None) -> Self:
        self.id = id
        return self

    def skip_id(self, id: str) -> Self:
        self.id = f"!{id}"
        return self

    def with_collision(self) -> Self:
        self.collision = True
        return self

    def no_collision(self) -> Self:
        self.collision = False
        return self

    def skip_collision(self) -> Self:
        self.collision = None
        return self

    def limit_by(self, limit: int) -> Self:
        self.limit = limit
        return self

    def return_as(self, return_type: type[dict|set|tuple|list]) -> Self:
        self.return_type = return_type
        return self

    def check(self, obj: Object) -> bool:
        check = True

        if self.obj_type is not None:
            check = isinstance(obj, self.obj_type)

        if self.layer is not None:
            check = obj.LAYER == self.layer

        if self.visible is not None:
            check = obj.VISIBLE == self.visible

        if self.with_handler is not None:
            check = obj.HANDLER_NAME is not None

        if self.id is not None:
            if check[0] == '!':
                check = obj.id != self.id[1:]
            else:
                check = obj.id == self.id

        return check


_all: dict[str, Object|Camera] = {}
_idx_visible: list[str] = []
_idx_main_layer: list[str] = []
_idx_hidden: list[str] = []
_idx_with_handlers: list[str] = []
_task_queue: list[_Task] = []


def clear() -> None:
    _all.clear()
    _idx_visible.clear()
    _idx_main_layer.clear()
    _idx_hidden.clear()
    _idx_with_handlers.clear()
    _task_queue.clear()


def add(obj: Object, throw: bool = False) -> None:
    if throw and obj.id in _all:
        raise KeyError(f"Object with id {obj.id} already exists.")

    _all[obj.id] = obj

    if obj.VISIBLE:
        _idx_visible.append(obj.id)
        _sort_visibles()
    else:
        _idx_hidden.append(obj.id)

    if obj.LAYER == Layer.MAIN and obj.id not in _idx_main_layer:
        _idx_main_layer.append(obj.id)

    if obj.HANDLER_NAME is not None:
        _idx_with_handlers.append(obj.id)


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

    if obj.HANDLER_NAME is not None:
        _idx_with_handlers.remove(obj.id)

    if obj.LAYER == Layer.MAIN and obj.id in _idx_main_layer:
        _idx_main_layer.remove(obj.id)

    return _all.pop(obj.id)


def all() -> dict[str, Object]:
    return _all


def get(id: str, throw: bool = False) -> Object|None:
    obj: Object|None = _all.get(id)

    if obj is None and throw:
        raise KeyError(f"Object with id {id} was not found.")

    return obj


def filter(filter: Filter) -> dict[str, Object]|Iterable[Object]|Object|None:
    if filter.limit == 1:
        return next(
            (obj for obj in _all.values() if filter.check(obj)),
            None
        )

    obtained = set(obj for obj in _all.values() if filter.check(obj))

    if filter.return_type == type[tuple]:
        return tuple(obtained)
    elif filter.return_type == type[list]:
        return list(obtained)
    elif filter.return_type == type[dict]:
        return {obj.id: obj for obj in obtained}
    else:
        return obtained


def visible() -> dict[str, Object]:
    return {obj_id: _all[obj_id] for obj_id in _idx_visible}


def main_layer() -> dict[str, Object]:
    return {obj_id: _all[obj_id] for obj_id in _idx_main_layer}


def dinosaurs(family: type[Dinosaur] = Dinosaur) -> dict[str, Dinosaur]:
    return {obj_id: _all[obj_id] for obj_id in _idx_visible if isinstance(_all[obj_id], family)}


def hidden() -> dict[str, Object]:
    return {obj_id: _all[obj_id] for obj_id in _idx_hidden}


def with_handlers() -> dict[str, Object]:
    return {obj_id: _all[obj_id] for obj_id in _idx_with_handlers}


def queue_add(obj: Object, throw: bool = False) -> None:
    new_task: _Task = _Task(_TaskType.ADD, obj)

    existing_task: _Task|None = next(
        (task for task in _task_queue if task.type == _TaskType.ADD and task.subject.id == obj.id),
        None
    )

    if existing_task is not None:
        if throw:
            raise KeyError(f"Addition of object with id {obj.id} is already queued.")
        else:
            _task_queue.remove(existing_task)

    _task_queue.append(new_task)


def queue_delete(obj: Object, throw: bool = False) -> None:
    new_task: _Task = _Task(_TaskType.DELETE, obj)

    existing_task: _Task | None = next(
        (task for task in _task_queue if task.type == _TaskType.DELETE and task.subject == obj.id),
        None
    )

    if existing_task is not None:
        if throw:
            raise KeyError(f"Removal of object with id {obj.id} is already queued.")
        else:
            _task_queue.remove(existing_task)

    _task_queue.append(new_task)


def process_task_queue() -> None:
    for task in _task_queue:
        if task.type == _TaskType.ADD:
            add(task.subject, task.throw)
        else:
            delete(task.subject, task.throw)

    _task_queue.clear()


def get_camera() -> Camera:
    return get(Camera.ID, True)


def get_player() -> TRexNew|TRexNewCave:
    return get(TRexNew.ID, True)


def get_ground() -> Ground:
    return get(Ground.ID, True)


def reset_updated_at() -> None:
    for obj in _all.values():
        obj.reset_last_update()


def _sort_visibles() -> None:
    global _idx_visible
    _idx_visible = sorted(_idx_visible, key=lambda obj: get(obj).LAYER)
