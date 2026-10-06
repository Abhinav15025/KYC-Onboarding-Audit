from datetime import date, timedelta

from src.validation_engine import (
    validate_required,
    validate_tax_id,
    validate_registration_number,
    validate_email,
    validate_phone,
    validate_document_number,
    validate_expiry_date
)


def test_required_field():

    assert validate_required("ABC") is True
    assert validate_required("") is False
    assert validate_required(None) is False


def test_tax_id():

    assert validate_tax_id("TAX123456789") is True
    assert validate_tax_id("INVALID-TAX") is False
    assert validate_tax_id(None) is False


def test_registration_number():

    assert validate_registration_number("REG123456") is True
    assert validate_registration_number("REG12ABC") is False
    assert validate_registration_number(None) is False


def test_email():

    assert validate_email("company@example.com") is True
    assert validate_email("invalid-email") is False


def test_phone():

    assert validate_phone("+91 98765 43210") is True
    assert validate_phone("123") is False


def test_document_number():

    assert validate_document_number("BUS-123456") is True
    assert validate_document_number("INVALID-DOC") is False


def test_expiry_date():

    future_date = date.today() + timedelta(days=30)
    past_date = date.today() - timedelta(days=30)

    assert validate_expiry_date(future_date) is True
    assert validate_expiry_date(past_date) is False