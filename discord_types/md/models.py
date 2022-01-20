from __future__ import annotations

import re
from typing import Any, Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel

from .mistune_types import Element, Heading, Paragraph


class Endpoint(BaseModel):
    name: str
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    route: str
    parameters: Dict[str, Optional[str]]
    description: str = ""
    return_type: Optional[str] = None

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

    @staticmethod
    def extract_description(elements: List[Element]) -> str:
        assert all(not isinstance(e, Heading) for e in elements)
        return "\n".join(p.text for p in elements if isinstance(p, Paragraph))

    @staticmethod
    def extract_returntype(description: str) -> Optional[str]:
        matches = list(
            re.finditer(
                r"[Rr]eturn[^\.;:]*?(?P<link>\[.+?\]\(.+?\)).*?[\.;:]", description, re.DOTALL
            )
        )
        if not matches:
            return None

        types = [m["link"] for m in matches]
        assert len(set(types)) == 1, f"found different return types: {types}"

        match = matches[0]
        ret = match["link"]
        if any(x in match.group().lower() for x in ("list of", "array of")):
            return f"list of {ret}"
        return ret
