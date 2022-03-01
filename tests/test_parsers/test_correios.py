import json
import pytest
from pytest_mock import MockerFixture
from django.core.exceptions import ValidationError
from brazilian_zipcode.parsers.correios import CorreiosParser
from brazilian_zipcode import BrazilianAddress


class FakeRequests:
    def __init__(self, example_json_path: str):
        self.example_json_path = example_json_path

    def json(self):
        with open(self.example_json_path, "r") as f:
            return json.load(f)

    def post(self, *args, **kwargs):
        return self


def test_invalid_zipcode_raises_validation_error(mocker: MockerFixture):
    mocker.patch(
        "brazilian_address.parsers.correios.requests",
        FakeRequests("examples/correios_bad_response.json"),
    )
    with pytest.raises(ValidationError):
        CorreiosParser.get_address_info("000000000")


def test_valid_zipcode_not_raises_validation_error(
    mocker: MockerFixture, valid_zipcode
):
    mocker.patch(
        "brazilian_address.parsers.correios.requests",
        FakeRequests("examples/correios_good_response.json"),
    )
    CorreiosParser.get_address_info(valid_zipcode)


def test_valid_zipcode_returns_correct_type(mocker: MockerFixture, valid_zipcode):
    mocker.patch(
        "brazilian_address.parsers.correios.requests",
        FakeRequests("examples/correios_good_response.json"),
    )
    address = CorreiosParser.get_address_info(valid_zipcode)
    assert isinstance(address, BrazilianAddress)
