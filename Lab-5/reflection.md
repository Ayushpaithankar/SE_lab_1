# Reflection

The supplied handout states that four reflection answers are required but does
not print four separate questions. The questions below follow the handout's
four practical learning themes: purpose, tool use, report interpretation, and
impact on maintainability.

## 1. What is the purpose and scope of static code analysis?

Static analysis examines source code without needing to exercise every runtime
path. It can identify security risks, likely bugs, inconsistent style, and
maintainability problems early in development. Its scope is broader than
formatting: in this program it exposed arbitrary code execution, shell command
injection, weak hashing, hidden exceptions, shared mutable state, and unsafe
resource handling. It does not prove that the program is correct, so runtime
and functional tests are still necessary.

## 2. How did Pylint, Bandit, and Flake8 contribute differently?

Bandit provided the most security-specific results. It identified the
`os.system()` injection risk, `eval()`, MD5, predictable randomness, the
hard-coded token, and the swallowed exception. Pylint found deeper quality and
design problems such as the mutable default argument, missing documentation,
resource handling, naming, dead code, and unnecessary control flow. Flake8
gave a focused PEP 8 and correctness check for the unused import and variable,
line length, bare exception, invalid `None` comparison, and missing final
newline. The overlap between tools increased confidence that important fixes
were not missed.

## 3. How were the reports interpreted and prioritized?

I reviewed High-severity findings first, followed by Medium findings, as the
handout requires. This meant removing shell execution and replacing MD5 before
addressing `eval()`. I then fixed all remaining Bandit findings rather than
stopping after four issues. Reliability bugs came next, especially the mutable
default argument and silent exception. Style-only findings were resolved last.
After each group of changes I reran the program and the relevant analyzer,
then produced final reports only when Bandit and Flake8 were clean and Pylint
reached 10.00/10.

## 4. How did the fixes improve quality and maintainability, and what are the limitations?

The cleaned program has a smaller attack surface and clearer contracts.
Seasonal pricing accepts a validated number instead of executable text,
booking references use secure randomness, and ledger export no longer invokes
a shell. Explicit return values make cancellation failures visible, context
management makes file output safer, and docstrings plus consistent naming make
the code easier to understand. A clean analyzer report is not the same as a
complete test suite: business rules, concurrency, persistence, user input,
and collision handling would still need dedicated tests in a production hotel
system.
