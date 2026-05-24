import sys

from storage.environment_check import print_environment_info, validate_dependencies


def test_print_environment_info() -> None:
    info = print_environment_info()
    assert info["python_executable"] == sys.executable
    assert isinstance(info["python_version"], str)
    assert info["python_version"]


def test_validate_dependencies_shape() -> None:
    result = validate_dependencies()
    assert "all_installed" in result
    assert "dependencies" in result
    assert set(result["dependencies"].keys()) == {"requests", "pytest", "dotenv"}


def test_validate_dependencies_values_boolean() -> None:
    result = validate_dependencies()
    for value in result["dependencies"].values():
        assert isinstance(value, bool)
