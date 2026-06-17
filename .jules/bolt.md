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

## 2026-06-03 - [Optimization: Shared Response Pre-allocation and Mutation Safety]
**Learning:** Pre-allocating common response dictionaries (like 404 errors) reduces object creation overhead. However, returning a direct reference to a mutable pre-allocated dictionary is dangerous as callers can mutate the shared state. Using `.copy()` preserves the performance benefit of not recreating the dictionary from a literal while ensuring safety.
**Action:** When pre-allocating mutable objects for reuse, always return a `.copy()` to prevent accidental shared state mutation.

## 2026-06-04 - [Optimization: Avoid Redundant $PATH Lookups]
**Learning:** When using `shutil.which` to verify a binary exists before calling it with `subprocess.run`, the second call performs another `$PATH` lookup if only the binary name is provided. Capturing the absolute path from `shutil.which` and passing it to `subprocess.run` avoids this redundant search. Benchmarks showed a ~10% improvement in execution time for these check patterns.
**Action:** Always capture and reuse the absolute path returned by `shutil.which` when subsequent process execution is required.

## 2026-06-05 - [Optimization: Dictionary-Based Routing and Pre-allocation]
**Learning:** In high-traffic API request handlers, replacing a set-based membership check and runtime template merging with a direct dictionary lookup of pre-allocated response objects provides a measurable performance gain (~8.8%). However, manual duplication of response structures can hurt maintainability.
**Action:** Use dictionary comprehensions to pre-allocate fully constructed response objects from a common template during initialization. This achieves the performance benefits of direct lookups while keeping the code DRY and maintainable.
