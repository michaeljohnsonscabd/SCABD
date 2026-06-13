# Bolt's Journal - Critical Learnings

## 2026-05-31 - [Optimization: find_spec vs __import__]
**Learning:** Using `importlib.util.find_spec` is significantly faster than `__import__` for checking dependency existence because it doesn't execute the module's code. This is especially impactful for heavy libraries like `pandas` or `sqlalchemy` which have extensive initialization logic.
**Action:** Prefer `importlib.util.find_spec` for diagnostic checks or lazy-loading existence checks.

## 2026-06-01 - [Optimization: O(1) Blocklist Lookups]
**Learning:** In the `BottyGuard` implementation, `threat_db` was originally a list, resulting in $O(n)$ lookup complexity. Switching to a `set` provided an $O(1)$ lookup time and reduced repeated IP storage. Additionally, an early return in the traffic monitor for already-identified threats prevents unnecessary signature processing.
**Action:** Use sets for high-frequency lookup containers (like blocklists or allowlists). Implement early return patterns for already-known states to minimize redundant computation.

## 2026-06-02 - [Optimization: High-Precision Timing and Fast Binary Checks]
**Learning:** For performance-critical duration measurements, `time.perf_counter()` is more efficient and provides higher resolution than `datetime.datetime.now()`. While `shutil.which` is faster for identifying missing binaries (avoiding `subprocess.run` fork/exec overhead), it can add redundant overhead in the success path if not handled carefully.
**Action:** Prefer `time.perf_counter()` for measuring durations. Use `shutil.which` primarily for early-exit checks where a missing tool is a likely and critical failure mode.

## 2026-06-03 - [Optimization: O(1) API Endpoint Lookups]
**Learning:** For API-first architectures, endpoint routing or validation using list lookups results in $O(n)$ complexity. As the number of endpoints grows, this can become a bottleneck in the request handling hot path. Converting the endpoint collection to a `set` provides $O(1)$ average-time complexity for existence checks.
**Action:** Use `set` for collections used primarily for membership testing, especially in performance-sensitive routing or validation logic.
