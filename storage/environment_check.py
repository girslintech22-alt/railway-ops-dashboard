from __future__ import annotations

import importlib
import platform
import sys
from typing import Any


def print_environment_info() -> dict[str, str]:
    """Return and print active Python environment details."""
    info: dict[str, str] = {
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "implementation": platform.python_implementation(),
    }
    for key, value in info.items():
        print(f"{key}: {value}")
    return info


def validate_dependencies() -> dict[str, Any]:
    """Validate availability of required runtime dependencies."""
    required: tuple[str, ...] = ("requests", "pytest", "dotenv")
    status: dict[str, Any] = {
        "all_installed": True,
        "dependencies": {},
    }

    for package in required:
        try:
            importlib.import_module(package)
            status["dependencies"][package] = True
        except Exception:
            status["dependencies"][package] = False
            status["all_installed"] = False

    return status


if __name__ == "__main__":
    print_environment_info()
    result = validate_dependencies()
    print(result)
