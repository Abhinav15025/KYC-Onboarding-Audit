from src.exception_manager import determine_severity


def test_high_severity():

    assert (
        determine_severity("DOCUMENT_EXPIRY")
        == "HIGH"
    )


def test_medium_severity():

    assert (
        determine_severity("TAX_ID_FORMAT")
        == "MEDIUM"
    )


def test_low_severity():

    assert (
        determine_severity("EMAIL_FORMAT")
        == "LOW"
    )