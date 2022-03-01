from dataclasses import dataclass


@dataclass(frozen=True)
class BrazilianAddress:
    zipcode: str
    street: str
    district: str
    city: str
    state_initials: str
