from typing import Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from .base import *
from .table import *

Element = Annotated[
    Union[
        Heading,
        Newline,
        BlockQuote,
        BlockCode,
        Paragraph,
        List,
        Table,
    ],
    Field(discriminator="type"),
]


for model_class in [
    c
    for c in vars().values()
    if (isinstance(c, type) and issubclass(c, BaseModel) and c.__module__.startswith(__name__))
]:
    model_class.update_forward_refs()
