"""Branch-coverage tests for the warranty-claims application."""

import pytest

from warranty_claims import claim_allowed, out_of_warranty_charge, sla_status


def test_unknown_plan_branch():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 12, "defect", False)


def test_negative_age_branch():
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


@pytest.mark.parametrize(
    ("plan", "age_months", "claim_type", "is_registered", "expected"),
    [
        # Covered, registered-extension and premium-plan branches.
        ("basic", 12, "defect", False, 0),
        ("standard", 30, "defect", True, 0),
        ("premium", 36, "defect", True, 0),
        # Accidental/defect and short/long excess branches.
        ("basic", 13, "defect", False, 100),
        ("basic", 13, "accidental", False, 200),
        ("basic", 25, "defect", False, 1_950),
        ("basic", 25, "accidental", False, 3_575),
    ],
)
def test_every_warranty_charge_branch(
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
        (0, 6, True, False),
        (29, 0, False, False),
        (30, 2, False, True),
        (30, 3, False, False),
    ],
)
def test_every_claim_allowed_branch(
    days_since_last_claim, claims_filed, is_recall, expected
):
    assert (
        claim_allowed(days_since_last_claim, claims_filed, is_recall) is expected
    )


@pytest.mark.parametrize(
    ("hours_left", "is_hardware", "is_priority", "expected"),
    [
        (48, True, False, "on_track"),
        (36, True, False, "at_risk"),
        (35, True, False, "critical"),
        (24, False, False, "on_track"),
        (36, False, True, "at_risk"),
        (35, False, True, "critical"),
    ],
)
def test_every_sla_status_branch(
    hours_left, is_hardware, is_priority, expected
):
    assert sla_status(hours_left, is_hardware, is_priority) == expected
