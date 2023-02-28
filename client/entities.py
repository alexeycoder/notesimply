from typing import Any, Callable, NamedTuple, Optional


class MenuItem(NamedTuple):
    name: str
    handler: Callable


class MenuModel(NamedTuple):
    header: Optional[str]
    items: dict[Any, MenuItem]
