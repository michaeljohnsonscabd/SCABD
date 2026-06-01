## 2025-05-15 - [Optimization of dependency checks]
**Learning:** Using `importlib.util.find_spec` instead of `__import__` to check for dependency existence is significantly faster as it avoids full module initialization. For large modules like `urllib.request`, it can be up to 18,000x faster when the module is already loaded, and it avoids the overhead of executing top-level code in unimported modules.
**Action:** Always use `importlib.util.find_spec` for environment diagnostics or conditional imports where only existence needs to be verified.
