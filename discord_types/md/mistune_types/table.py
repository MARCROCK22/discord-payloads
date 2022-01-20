from __future__ import annotations

import typing as t

from .base import BaseElement, _TextProp


class Table(BaseElement):
    type: t.Literal["table"]
    children: t.Tuple[TableRow, TableBody]


class TableBody(BaseElement):
    type: t.Literal["table_body"]
    children: t.List[TableRow]


class TableRow(BaseElement):
    type: t.Literal["table_head", "table_row"]
    children: t.List[TableCell]


class TableCell(BaseElement):
    type: t.Literal["table_cell"]
    text: str = _TextProp
    align: t.Optional[t.Literal["left", "center", "right"]]
    is_head: bool
