from typing import Any, Dict, List

import mistune
from pydantic import parse_obj_as

from .mistune_types import Element


class _FakeInline:
    def __init__(self, renderer: mistune.renderers.BaseRenderer):
        self.renderer = renderer

    def __call__(self, token: Any, *args: Any) -> Any:
        return token


def ast(md: str) -> List[Element]:
    renderer = mistune.AstRenderer()
    obj = mistune.Markdown(
        renderer,
        # stub inline parser, since we don't really care about inline markdown (``, **, __, [](), etc.)
        inline=_FakeInline(renderer),
        plugins=[mistune.plugins.plugin_table],
    )
    ast: List[Dict[str, Any]] = obj.parse(md)
    return parse_obj_as(List[Element], ast)
