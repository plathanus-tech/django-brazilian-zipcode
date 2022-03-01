from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from brazilian_zipcode import BrazilianAddress


class BaseParser(Protocol):
    def get_address_info(cls, address: str) -> "BrazilianAddress":
        raise NotImplementedError(
            "This method should be implemented on the child class."
        )
