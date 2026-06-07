# Bolt's Journal - Critical Learnings

## 2026-05-31 - [Optimization: find_spec vs __import__]
**Learning:** Using `importlib.util.find_spec` is significantly faster than `__import__` for checking dependency existence because it doesn't execute the module's code. This is especially impactful for heavy libraries like `pandas` or `sqlalchemy` which have extensive initialization logic.
**Action:** Prefer `importlib.util.find_spec` for diagnostic checks or lazy-loading existence checks.

## 2026-06-07 - [Optimization: Set vs List for Security Blocklists]
**Learning:** Using a `set` for security blocklists (like `threat_db`) provides O(1) average-case lookup time compared to O(n) for a `list`. In benchmarks with 1,000 entries and 100,000 lookups, switching to a `set` reduced execution time from ~1.11s to ~0.007s (a 99.4% improvement).
**Action:** Always use `set` or `dict` for frequently queried membership checks, especially in high-traffic paths like security filtering.
