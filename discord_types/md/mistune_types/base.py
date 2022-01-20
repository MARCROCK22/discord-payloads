from __future__ import annotations

import typing as t

from pydantic import BaseModel, Extra, Field

_TextProp = Field(alias="children")


class BaseElement(BaseModel):
    type: str

    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid


class Heading(BaseElement):
    type: t.Literal["heading"]
    text: str = _TextProp
    level: int


class Newline(BaseElement):
    type: t.Literal["newline"]


class BlockQuote(BaseElement):
    type: t.Literal["block_quote"]
    children: t.Tuple[Paragraph]


class BlockCode(BaseElement):
    type: t.Literal["block_code"]
    text: str
    info: t.Optional[str]


class BlockText(BaseElement):
    type: t.Literal["block_text"]
    text: str = _TextProp


class Paragraph(BaseElement):
    type: t.Literal["paragraph"]
    text: str = _TextProp


class Link(BaseElement):
    type: t.Literal["link"]
    text: str = _TextProp
    link: str
    title: t.Optional[str]


class List(BaseElement):
    type: t.Literal["list"]
    children: t.List[ListItem]
    ordered: bool
    level: int


class ListItem(BaseElement):
    type: t.Literal["list_item"]
    children: t.List[t.Union[BlockText, List]]
    level: int
