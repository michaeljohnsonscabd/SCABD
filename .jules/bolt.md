# Bolt's Journal - Critical Learnings

## 2026-05-31 - [Optimization: find_spec vs __import__]
**Learning:** Using `importlib.util.find_spec` is significantly faster than `__import__` for checking dependency existence because it doesn't execute the module's code. This is especially impactful for heavy libraries like `pandas` or `sqlalchemy` which have extensive initialization logic.
**Action:** Prefer `importlib.util.find_spec` for diagnostic checks or lazy-loading existence checks.

## 2026-06-01 - [Optimization: Set-based Blocklist]
**Learning:** Using a `set` for threat databases provides O(1) lookup time, which is critical for high-traffic security filters. Additionally, an early return in the traffic monitor avoids redundant processing of already-blocked IPs and prevents duplicate entries, which in this case improved performance by ~300x with 5000 blocked IPs.
**Action:** Always prefer `set` for unique identifier lookups (like IPs or IDs) and use early return patterns to bypass logic for already-processed entities.
