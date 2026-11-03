# Lab 6: Code and Branch Coverage Analysis

This submission tests the assigned `warranty_claims.py` application without
changing its behaviour.

## Code coverage

Run the dedicated line-coverage test suite from this directory:

```bash
coverage erase
coverage run -m pytest CodeCoverageTest_warranty_claims_application.py
coverage report -m warranty_claims.py
```

The final terminal output is saved in `code_coverage_terminal.png`.

## Branch coverage

Run the dedicated branch-coverage test suite from this directory:

```bash
coverage erase
coverage run --branch -m pytest BranchCoverageTest_warranty_claims_application.py
coverage report -m warranty_claims.py
```

The final terminal output is saved in `branch_coverage_terminal.png`.

## Final results

| Analysis | Tests passed | Coverage |
|---|---:|---:|
| Code (statement) coverage | 15 | 100% |
| Branch coverage | 20 | 100% |

## Requirements

```bash
python -m pip install -r requirements.txt
```
