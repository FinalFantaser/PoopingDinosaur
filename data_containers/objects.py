from enum import Enum
import pygame.time
from objects import Object, Camera, Allosaurus, Ground


class _TaskType(int, Enum):
    ADD = 0
    DELETE = 1



class _Task:
    __slots__ = ("type", "subject", "throw")
    def __init__(self, type: _TaskType, subject: Object | str, throw: bool = False) -> None:
        self.type: _TaskType = type
        self.subject: Object|str = subject
        self.throw: bool = throw


_all: dict[str, Object|Camera] = {}
_idx_visible: list[str] = []
_idx_hidden: list[str] = []
_idx_with_handlers: list[str] = []
_task_queue: list[_Task] = []


def clear() -> None:
    _all.clear()
    _idx_visible.clear()
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

    return _all.pop(obj.id)


def all() -> dict[str, Object]:
    return _all


def get(id: str, throw: bool = False) -> Object|None:
    obj: Object|None = _all.get(id)

    if obj is None and throw:
        raise KeyError(f"Object with id {id} was not found.")

    return obj


def visible() -> dict[str, Object]:
    return {obj_id: _all[obj_id] for obj_id in _idx_visible}


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


def get_player() -> Allosaurus:
    return get(Allosaurus.ID, True)


def get_ground() -> Ground:
    return get(Ground.ID, True)


def reset_updated_at() -> None:
    for obj in _all.values():
        obj.reset_last_update()


def _sort_visibles() -> None:
    global _idx_visible
    _idx_visible = sorted(_idx_visible, key=lambda obj: get(obj).LAYER)