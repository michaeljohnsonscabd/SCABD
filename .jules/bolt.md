# Bolt's Journal - Critical Learnings

## 2026-05-31 - [Optimization: find_spec vs __import__]
**Learning:** Using `importlib.util.find_spec` is significantly faster than `__import__` for checking dependency existence because it doesn't execute the module's code. This is especially impactful for heavy libraries like `pandas` or `sqlalchemy` which have extensive initialization logic.
**Action:** Prefer `importlib.util.find_spec` for diagnostic checks or lazy-loading existence checks.

## 2026-06-01 - [Optimization: O(1) Blocklist Lookups]
**Learning:** Using a `set` for threat blocklists instead of a `list` provides constant time $O(1)$ lookups, which is critical for security modules that process high volumes of traffic. Additionally, implementing an early return for already-blocked IPs prevents redundant signature checking and logging.
**Action:** Use sets for membership-heavy collections and prioritize early returns for known states.
