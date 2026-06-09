# Bolt's Journal - Critical Learnings

## 2026-05-31 - [Optimization: find_spec vs __import__]
**Learning:** Using `importlib.util.find_spec` is significantly faster than `__import__` for checking dependency existence because it doesn't execute the module's code. This is especially impactful for heavy libraries like `pandas` or `sqlalchemy` which have extensive initialization logic.
**Action:** Prefer `importlib.util.find_spec` for diagnostic checks or lazy-loading existence checks.

## 2026-06-01 - [Optimization: O(1) Blocklist Lookups]
**Learning:** In the `BottyGuard` implementation, `threat_db` was originally a list, resulting in $O(n)$ lookup complexity. Switching to a `set` provided an $O(1)$ lookup time and reduced repeated IP storage. Additionally, an early return in the traffic monitor for already-identified threats prevents unnecessary signature processing.
**Action:** Use sets for high-frequency lookup containers (like blocklists or allowlists). Implement early return patterns for already-known states to minimize redundant computation.

## 2026-06-02 - [Optimization: shutil.which vs subprocess.run]
**Learning:** Using `shutil.which` to verify the existence of external binaries before execution is significantly faster (~0.19ms) than relying on `subprocess.run` to fail with `FileNotFoundError` (~0.61ms). It also prevents potential crashes if the error is not caught.
**Action:** Use `shutil.which` for existence checks of external tools, especially in diagnostic scripts where tools might be missing.

## 2026-06-02 - [Lesson: Micro-optimization vs JSON Serialization]
**Learning:** Converting a small list (e.g., < 5 elements) to a `set` for $O(1)$ lookup in an API layer is a micro-optimization with negligible gain. More importantly, Python `set` objects are not JSON serializable by default, which can cause runtime `TypeError` in API responses.
**Action:** Prioritize compatibility and serializability over micro-optimizations in API data structures. Only use sets for large collections or non-serialized internal state.
