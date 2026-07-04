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

## 2026-06-18 - [Optimization: Concise get().copy() in Hot Paths]
**Learning:** In high-traffic request handlers where a default response must be returned for missing keys, using `dict.get(key, default).copy()` is approximately 8% faster than a manual `if key in dict: return dict[key].copy() else: return default.copy()` pattern. This is due to reduced bytecode instructions, specifically by avoiding explicit branching and local variable assignments.
**Action:** Use `dict.get(key, default).copy()` for combined lookup and fallback operations on mutable objects to keep hot paths concise and efficient.

## 2026-06-25 - [Optimization: Memoization and Optimized Iteration in Diagnostics]
**Learning:** In the `DiagnosticsReport` class, generating a summary was an $O(N)$ operation that was called multiple times (for console output and JSON generation). Implementing memoization with cache invalidation ensures the calculation is only performed once per set of changes. Additionally, using `.values()` instead of `.items()` in nested loops provides a small performance boost by avoiding unused key lookups and tuple creation.
**Action:** Use memoization for expensive state-derived calculations that are accessed multiple times. Prefer `.values()` or `.keys()` over `.items()` when the full pair is not required.

## 2026-06-24 - [Optimization: Dictionary .copy() vs Unpacking in Init]
**Learning:** Using `.copy()` followed by manual key assignment is significantly faster (~45%) than dictionary unpacking (`{**template, ...}`) or union operators when pre-allocating multiple dictionaries from a template during class initialization. Unpacking creates intermediate objects and has more overhead than the optimized internal `copy()` method.
**Action:** Prefer `.copy()` and manual assignment for performance-sensitive dictionary pre-allocation in constructors.

## 2026-06-26 - [Optimization: Zero-Cost Exceptions for Hot Path Lookups]
**Learning:** In Python 3.11+, "zero-cost" exceptions mean that `try` blocks have virtually no overhead if no exception is raised. In high-traffic dictionary lookups where the "hit" rate is high, a `try...except KeyError` pattern outperforms `dict.get()` by avoiding a function call and internal checks. Benchmarks showed a ~14% performance improvement in the happy path. However, the penalty for a miss (exception being raised) is significant (over 100%).
**Action:** Use `try...except KeyError` for dictionary lookups in hot paths where successful lookups are the expected majority case.
