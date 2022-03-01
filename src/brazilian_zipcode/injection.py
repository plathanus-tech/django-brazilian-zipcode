import pydoc
from typing import Optional
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .parsers.base import BaseParser


def get_address_parser() -> BaseParser:
    try:
        Parser: Optional[BaseParser] = pydoc.locate(settings.ADDRESS_PARSER_CLASS)
        assert hasattr(Parser, "get_address_info") and callable(
            Parser.get_address_info
        ), f"Parser '{settings.ADDRESS_PARSER_CLASS}' does not implements `get_address_info`"

    except (AttributeError, ImproperlyConfigured):
        Parser = None

    if not Parser:
        from brazilian_zipcode.parsers.correios import CorreiosParser

        Parser = CorreiosParser
    return Parser
