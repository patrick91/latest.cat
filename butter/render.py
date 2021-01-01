import typing

from .components import Component


def attributes(component: Component) -> str:
    out = ""

    for name, value in component.attributes.items():
        out += f' {name}="{value}"'

    return out


def open_tag(component: Component) -> str:
    return f"<{component.tag_name}{attributes(component)}>"


def close_tag(component: Component) -> str:
    return f"</{component.tag_name}>"


def render(component: typing.Union[Component, str]) -> str:
    if type(component) == str:
        return typing.cast(str, component)

    component = typing.cast(Component, component)

    html = [open_tag(component)]

    for child in component.children:
        html.append(render(child))

    html += [close_tag(component)]

    return "".join(html)
