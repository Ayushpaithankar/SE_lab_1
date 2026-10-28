# Static Analysis Issue Log

Issues are ordered by severity, with the original line numbers from the provided
`hotel_booking_system.py`. All listed issues were fixed in the cleaned version.

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command injection risk | Security - High | 58 | `os.system()` joined an externally supplied filename into a shell command, allowing shell metacharacters to execute commands. Bandit B605. | Removed the shell call and used Python's `print()` to report the exported filename. |
| Weak MD5 guest hash | Security - High | 47 | MD5 is collision-prone and unsuitable for security-sensitive identifiers. Bandit B324. | Replaced MD5 with SHA-256 via `hashlib.sha256()`. |
| Arbitrary code execution with `eval` | Security - Medium | 40-43 | `eval(rate_expr)` could execute arbitrary Python supplied as a pricing expression. Bandit B307. | Changed the function to accept a validated, non-negative numeric multiplier and calculate the price directly. |
| Predictable booking references | Security - Low | 50-51 | `random.randint()` is predictable and unsuitable for reservation identifiers. Bandit B311. | Used `secrets.randbelow()` to generate a secure four-digit reference. |
| Hard-coded and disclosed secret | Security - Low | 62, 70 | An administrator token was embedded in source code and printed to standard output. Bandit B105. | Removed the unused token and its output entirely. |
| Broad exception silently ignored | Reliability/Security - Low | 23-27 | A bare `except` hid every error and then continued, making failed cancellations invisible. Pylint W0702 and Bandit B110. | Replaced exception swallowing with an explicit room-existence check and a Boolean result. |
| Mutable default argument | Bug | 15 | The default `booking_log=[]` was shared by every call, causing state to leak between bookings. Pylint W0102. | Changed the default to `None` and created a new list inside the function. |
| Unsafe file-resource handling | Reliability | 54-57 | The ledger file was manually opened and closed, so exceptions could leave it open; no encoding was specified. Pylint R1732/W1514. | Used a `with` context manager and explicitly selected UTF-8. |
| Incorrect style and dead code | Style | 6, 15, 19, 31-37, 73 | The script had an unused import/variable, a non-snake-case function, old string formatting, an unnecessary `else`, a `None` comparison, and no final newline. | Removed dead code, renamed `bookRoom` to `book_room`, used an f-string, simplified the return, used `is None`, and formatted the file to PEP 8. |
| Import side effect | Design | 73 | Calling `main()` unconditionally ran the demonstration whenever the module was imported. | Added an `if __name__ == "__main__":` guard. |

## Verification Summary

- Bandit: 6 findings before; 0 findings after.
- Pylint: 5.32/10 before; 10.00/10 after.
- Flake8: 7 findings before; 0 findings after.
