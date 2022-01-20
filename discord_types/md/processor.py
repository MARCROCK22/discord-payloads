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
        # if it's a heading, try to parse the endpoint URL
        if isinstance(el, Heading) and (endpoint := Endpoint.try_parse(el)):
            below = _get_elements(ast, index, single=True)
            endpoint.description = Endpoint.extract_description(below)
            endpoint.return_type = Endpoint.extract_returntype(endpoint.description)
            if endpoint.method == "GET" and not endpoint.return_type:
                print(f"Missing return type for {endpoint}")

            data.endpoints.append(endpoint)
            index += len(below)
        # elif ...:
        index += 1
    return data
