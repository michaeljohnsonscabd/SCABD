# Bolt's Journal - Critical Learnings

## 2026-05-31 - [Optimization: find_spec vs __import__]
**Learning:** Using `importlib.util.find_spec` is significantly faster than `__import__` for checking dependency existence because it doesn't execute the module's code. This is especially impactful for heavy libraries like `pandas` or `sqlalchemy` which have extensive initialization logic.
**Action:** Prefer `importlib.util.find_spec` for diagnostic checks or lazy-loading existence checks.

## 2026-06-01 - [Optimization: O(1) Blocklist Lookups]
**Learning:** In the `BottyGuard` implementation, `threat_db` was originally a list, resulting in $O(n)$ lookup complexity. Switching to a `set` provided an $O(1)$ lookup time and reduced repeated IP storage. Additionally, an early return in the traffic monitor for already-identified threats prevents unnecessary signature processing.
**Action:** Use sets for high-frequency lookup containers (like blocklists or allowlists). Implement early return patterns for already-known states to minimize redundant computation.

## 2026-06-10 - [Optimization: shutil.which and time.perf_counter]
**Learning:** Using `shutil.which` for binary existence checks is roughly 5-18x faster than using `subprocess.run` and catching `FileNotFoundError`. For measuring durations, `time.perf_counter()` is not only monotonic and more precise but also approximately 3x faster than `datetime.datetime.now()`.
**Action:** Use `shutil.which` to verify command existence before execution. Prefer `time.perf_counter()` for all performance-related duration measurements.
