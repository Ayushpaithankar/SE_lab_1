import math

from hypothesis import given, strategies as st

from warranty_claims import parse_claim, age_average, payable_charge


@given(st.text() | st.none())
def test_parse_claim_no_crash(s):
    plan, months = parse_claim(s)
    assert isinstance(plan, str)
    assert isinstance(months, float)
    assert math.isfinite(months)
    assert months >= 0


@given(st.text() | st.none())
def test_age_average_no_crash(s):
    average = age_average(s)
    assert isinstance(average, int)
    assert average >= 0


@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
    charge = payable_charge(s)
    assert isinstance(charge, float)
    assert math.isfinite(charge)
    assert charge >= 0


def test_valid_inputs_keep_original_behaviour():
    assert parse_claim(" standard :30") == ("Standard", 30.0)
    assert age_average("12,24,36") == 24
    assert payable_charge("1500|200") == 1570.0


def test_invalid_inputs_use_safe_defaults():
    assert parse_claim(None) == ("Unknown", 0.0)
    assert parse_claim("broken") == ("Unknown", 0.0)
    assert age_average(None) == 0
    assert age_average("12,,36") == 0
    assert payable_charge(None) == 0.0
    assert payable_charge("free") == 0.0
