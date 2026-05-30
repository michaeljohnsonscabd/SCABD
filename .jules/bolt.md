## 2025-05-14 - [Optimize dependency checks with find_spec]
**Learning:** Using `__import__(name)` to check for dependency existence triggers full module initialization, which is O(expensive) for large libraries like `pandas` or `sqlalchemy`. `importlib.util.find_spec(name)` provides a lightweight way to check for module presence without loading it.
**Action:** Always prefer `importlib.util.find_spec(module_name) is not None` over `try: __import__(module_name) except ImportError` when only checking for existence.
