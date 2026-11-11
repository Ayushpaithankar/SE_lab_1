# Lab 7 - Fuzz Testing Warranty Claims

This submission uses Hypothesis property-based testing to find and fix input-validation bugs in the assigned warranty-claims application.

## Run

```bash
python -m pip install -r requirements.txt
python warranty_claims.py
python -m pytest test_warranty_claims.py
```

## Defensive behavior

- `parse_claim`: malformed data returns `("Unknown", 0.0)`.
- `age_average`: malformed or negative ages return `0`.
- `payable_charge`: malformed, non-finite, or negative values return `0.0`.

Valid inputs retain the original behavior. The accompanying PDF report contains the required screenshots from the original run, failing fuzz run, fixed application run, and passing fuzz run.
