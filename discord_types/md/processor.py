from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .mistune_types import Element, Heading, Paragraph
from .models import Endpoint


class ProcessedData(BaseModel):
    endpoints: List[Endpoint] = []

    def __bool__(self) -> bool:
        return bool(self.endpoints)


def _get_elements(ast: List[Element], index: int, *, single: bool = False) -> List[Element]:
    heading = ast[index]
    assert isinstance(heading, Heading)

    for i in range(index + 1, len(ast)):
        el = ast[i]
        if isinstance(el, Heading) and (single or el.level <= heading.level):
            return ast[index + 1 : i]
    return ast[index + 1 :]


def read_ast(ast: List[Element]) -> ProcessedData:
    data = ProcessedData()
    index = 0
    while index < len(ast):
        el = ast[index]
        if isinstance(el, Heading) and (endpoint := Endpoint.try_parse(el)):
            below = _get_elements(ast, index, single=True)
            endpoint.description = "\n".join(p.text for p in below if isinstance(p, Paragraph))
            data.endpoints.append(endpoint)
            index += len(below)
        index += 1
    return data
