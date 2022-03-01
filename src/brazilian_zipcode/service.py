from typing import TYPE_CHECKING
from . import injection
from .parsers.base import BaseParser


if TYPE_CHECKING:
    from .objects import BrazilianAddress


def get_address_info(zipcode: str) -> "BrazilianAddress":
    Parser: BaseParser = injection.get_address_parser()
    return Parser.get_address_info(zipcode)
