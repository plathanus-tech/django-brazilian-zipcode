from django import forms
from .service import get_address_info


class BrazilianZipCodeField(forms.RegexField):
    REGEX_VALIDATOR = r"^\d{2}\.?\d{3}-?\d{3}$"

    def __init__(self, *args, **kwargs):
        super().__init__(self.REGEX_VALIDATOR, *args, **kwargs)

    def clean(self, value: str):
        value = super().clean(value)
        value = value.replace(".", "").replace("-", "")
        return get_address_info(value)
