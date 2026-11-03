"""Line-coverage tests for the warranty-claims application."""

import pytest

from warranty_claims import claim_allowed, out_of_warranty_charge, sla_status


def test_unknown_plan_is_rejected():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 12, "defect", False)


def test_negative_age_is_rejected():
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


@pytest.mark.parametrize(
    ("plan", "age_months", "claim_type", "is_registered", "expected"),
    [
        ("standard", 20, "defect", False, 0),
        ("standard", 30, "defect", True, 0),
        ("basic", 18, "accidental", False, 1_200),
        ("basic", 30, "defect", False, 2_700),
        ("basic", 30, "accidental", False, 4_950),
    ],
)
def test_out_of_warranty_charges(
    plan, age_months, claim_type, is_registered, expected
):
    assert (
        out_of_warranty_charge(plan, age_months, claim_type, is_registered)
        == expected
    )


@pytest.mark.parametrize(
    ("days_since_last_claim", "claims_filed", "is_recall", "expected"),
    [
        (0, 5, True, True),
        (10, 0, False, False),
        (30, 2, False, True),
        (60, 3, False, False),
    ],
)
def test_claim_eligibility(
    days_since_last_claim, claims_filed, is_recall, expected
):
    assert (
        claim_allowed(days_since_last_claim, claims_filed, is_recall) is expected
    )


@pytest.mark.parametrize(
    ("hours_left", "is_hardware", "is_priority", "expected"),
    [
        (48, True, False, "on_track"),
        (12, False, False, "at_risk"),
        (10, False, False, "critical"),
        (72, True, True, "on_track"),
    ],
)
def test_sla_status(hours_left, is_hardware, is_priority, expected):
    assert sla_status(hours_left, is_hardware, is_priority) == expected
