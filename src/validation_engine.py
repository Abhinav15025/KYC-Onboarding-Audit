import re
from datetime import date

def validate_required(value):

    return value is not None and str(value).strip() != ""


def validate_tax_id(tax_id):

    if not validate_required(tax_id):
        return False

    pattern = r"^TAX\d{9}$"

    return bool(re.match(pattern, str(tax_id)))


def validate_registration_number(registration_number):

    if not validate_required(registration_number):
        return False

    pattern = r"^REG\d{6}$"

    return bool(
        re.match(
            pattern,
            str(registration_number)
        )
    )


def validate_email(email):

    if not validate_required(email):
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return bool(
        re.match(
            pattern,
            str(email)
        )
    )


def validate_phone(phone):

    if not validate_required(phone):
        return False

    digits = re.sub(r"\D", "", str(phone))

    return len(digits) >= 7


def validate_document_number(document_number):

    if not validate_required(document_number):
        return False

    pattern = r"^[A-Z]{3}-\d{6}$"

    return bool(
        re.match(
            pattern,
            str(document_number)
        )
    )


def validate_expiry_date(expiry_date):

    if expiry_date is None:
        return False

    if hasattr(expiry_date, "date"):
        expiry_date = expiry_date.date()

    return expiry_date >= date.today()