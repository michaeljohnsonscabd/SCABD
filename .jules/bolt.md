# Bolt's Journal - SCABD Performance Optimizations

## 2025-05-29 - Initial Diagnostics Optimization
**Learning:** `shutil.which` is significantly faster than `subprocess.run` for checking if a command exists in the PATH, as it avoids spawning a new process. `importlib.util.find_spec` allows checking for the presence of a Python package without the overhead of importing it, which is especially beneficial for large libraries like `pandas` or `sqlalchemy`.
**Action:** Use `shutil.which` for command existence checks and `importlib.util.find_spec` for dependency checks in diagnostic scripts.
