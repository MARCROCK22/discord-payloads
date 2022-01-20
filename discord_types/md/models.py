from __future__ import annotations

import re
from typing import Any, Dict, Literal, Optional, Tuple

from pydantic import BaseModel

from .mistune_types import Heading


class Endpoint(BaseModel):
    name: str
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    route: str
    parameters: Dict[str, Optional[str]]
    description: str = ""

    @classmethod
    def try_parse(cls, heading: Heading) -> Optional[Endpoint]:
        match = re.match(r"(?P<name>.+) % (?P<method>.+?) (?P<route>.+)", heading.text)
        if not match:
            return None
        data: Dict[str, Any] = match.groupdict()
        data["route"], data["parameters"] = cls.extract_params(data["route"])
        return Endpoint(**data)

    @staticmethod
    def extract_params(route: str) -> Tuple[str, Dict[str, Optional[str]]]:
        def repl(match: re.Match[str]) -> str:
            name: str = match["name"]
            link: Optional[str] = match["link"]
            assert name not in params
            params[name] = link
            return f"{{{name}}}"

        params: Dict[str, Optional[str]] = {}
        route = re.sub(r"\{(?P<name>[^#}]+)(?:#(?P<link>[^}]+))?\}", repl, route)
        return route, params
