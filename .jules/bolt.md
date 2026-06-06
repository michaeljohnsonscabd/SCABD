# Bolt's Journal - Critical Learnings

## 2026-05-31 - [Optimization: find_spec vs __import__]
**Learning:** Using `importlib.util.find_spec` is significantly faster than `__import__` for checking dependency existence because it doesn't execute the module's code. This is especially impactful for heavy libraries like `pandas` or `sqlalchemy` which have extensive initialization logic.
**Action:** Prefer `importlib.util.find_spec` for diagnostic checks or lazy-loading existence checks.

## 2026-06-01 - [Optimization: O(1) IP filtering with set]
**Learning:** In 'security/botty_guard/guard.py', using a 'set' for 'threat_db' instead of a 'list' drastically improves performance for repeat offenders. It reduces complexity from O(n) to O(1) for lookups and prevents memory bloat by automatically handling duplicates. An early return pattern in 'monitor_traffic' further saves CPU by skipping signature analysis for already-blocked IPs.
**Action:** Use sets for membership lookups in security filtering and implement early returns for known states.
