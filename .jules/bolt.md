# Bolt's Journal - Critical Learnings

## 2026-05-31 - [Optimization: find_spec vs __import__]
**Learning:** Using `importlib.util.find_spec` is significantly faster than `__import__` for checking dependency existence because it doesn't execute the module's code. This is especially impactful for heavy libraries like `pandas` or `sqlalchemy` which have extensive initialization logic.
**Action:** Prefer `importlib.util.find_spec` for diagnostic checks or lazy-loading existence checks.

## 2026-06-01 - [Optimization: Set for Membership Lookups]
**Learning:** In the `BottyGuard` implementation, using a `set` instead of a `list` for the `threat_db` improved membership lookup time from $O(n)$ to $O(1)$. This is critical for high-traffic security components where the same malicious IPs may hit the system repeatedly.
**Action:** Use sets for collections where unique membership checks are a frequent "hot path" operation.
