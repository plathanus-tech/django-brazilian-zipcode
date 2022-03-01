import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from brazilian_zipcode import BrazilianAddress


class CorreiosParser:
    URL = "https://buscacepinter.correios.com.br/app/endereco/carrega-cep-endereco.php"

    @classmethod
    def get_address_info(cls, address: str) -> BrazilianAddress:
        try:
            response = requests.post(
                cls.URL,
                data={
                    "pagina": "/app/endereco/index.php",
                    "endereco": address,
                    "tipoCEP": "ALL",
                },
            )
        except Exception:
            raise ValidationError(_("Search service unavailable."))

        try:
            jsn = response.json()
            dados = jsn["dados"][0]
        except Exception:
            raise ValidationError(_("Zipcode not found"))

        return BrazilianAddress(
            zipcode=address,
            street=dados["logradouroDNEC"],
            district=dados["bairro"],
            city=dados["localidade"],
            state_initials=dados["uf"],
        )
