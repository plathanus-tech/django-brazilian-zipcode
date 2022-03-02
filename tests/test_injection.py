import pytest
from pytest_mock import MockerFixture
from brazilian_zipcode.injection import get_address_parser
from brazilian_zipcode.parsers.correios import CorreiosParser


def test_no_settings_returns_correios_parser():
    Parser = get_address_parser()

    assert Parser is CorreiosParser


class TestParser:
    @classmethod
    def get_address_info(cls, address):
        ...


class FakeSettings:
    ADDRESS_PARSER_CLASS = "tests.test_injection.TestParser"


def test_with_settings_returns_desired_class(mocker: MockerFixture):
    mocker.patch("brazilian_zipcode.injection.settings", FakeSettings)
    Parser = get_address_parser()
    assert Parser is TestParser


class TestParserNoMethod:
    pass


class FakeSettingsParserNoMethod:
    ADDRESS_PARSER_CLASS = "tests.test_injection.TestParserNoMethod"


def test_with_settings_parser_without_get_address_info_raises_assertion_error(
    mocker: MockerFixture,
):
    mocker.patch("brazilian_zipcode.injection.settings", FakeSettingsParserNoMethod)
    with pytest.raises(AssertionError):
        get_address_parser()
