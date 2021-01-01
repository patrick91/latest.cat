from __future__ import annotations

import dataclasses
from typing import Any, Callable, Dict, List, Optional


@dataclasses.dataclass
class Component:
    tag_name: str
    attributes: Dict[str, Any] = dataclasses.field(default_factory=dict)
    children: List[Component] = dataclasses.field(default_factory=list, init=False)
    parent: Optional[Component] = dataclasses.field(default=None, init=False)

    def __gt__(self, value):
        if type(value) not in (str, Component, list):
            raise ValueError(f"Cannot nest type of {type(value)}")

        if type(value) == Component:
            value.parent = self

        if type(value) == list:
            self.children = value
        else:
            self.children = [value]

        r = self

        while r.parent is not None:
            r = r.parent

        return r


def div():
    return Component("div")


def header():
    return Component("header")


def p():
    return Component("p")


def main():
    return Component("main")


def _make_component(tag_name: str) -> Callable[[Dict[str, Any]], Component]:
    def f(**kwargs):
        return Component(tag_name, attributes=kwargs)

    f.__name__ == tag_name

    return f


html = _make_component("html")
body = _make_component("body")
head = _make_component("head")
style = _make_component("style")
link = _make_component("link")
h1 = _make_component("h1")
h2 = _make_component("h2")
h3 = _make_component("h3")
h4 = _make_component("h4")
h5 = _make_component("h5")
h6 = _make_component("h6")
form = _make_component("form")
input = _make_component("input")
button = _make_component("button")
span = _make_component("span")
svg = _make_component("svg")
path = _make_component("path")
