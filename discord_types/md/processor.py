from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .mistune_types import Element, Heading
from .models import Endpoint


class ProcessedData(BaseModel):
    endpoints: List[Endpoint] = []

    def __bool__(self) -> bool:
        return bool(self.endpoints)


def read_ast(ast: List[Element]) -> ProcessedData:
    data = ProcessedData()
    for el in ast:
        if isinstance(el, Heading) and (endpoint := Endpoint.try_parse(el)):
            data.endpoints.append(endpoint)
    return data
