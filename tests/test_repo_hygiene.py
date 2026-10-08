"""Repository-wide sanity checks for SAKURA.

The scripts in this repository mostly need a CMSSW release, ROOT or access to
CERN services to actually run, so they cannot be executed in a plain GitHub
Actions runner. What *can* be checked there is that every tracked file is
syntactically valid and that the data/config files we ship parse: that is what
these tests do.

Run them locally with:

    pytest tests -q
"""

import json
import py_compile
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def tracked(*patterns):
    """Return the git-tracked files matching any of the given pathspecs."""
    result = subprocess.run(
        ["git", "ls-files", "-z", *patterns],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        check=True,
    )
    return [REPO_ROOT / name for name in result.stdout.decode().split("\0") if name]


def ids(paths):
    return [str(path.relative_to(REPO_ROOT)) for path in paths]


PYTHON_FILES = tracked("*.py")
SHELL_FILES = tracked("*.sh")
JSON_FILES = tracked("*.json", "*.jsn")
YAML_FILES = tracked("*.yaml", "*.yml")
REQUIREMENT_FILES = tracked("*requirements.txt")


def test_files_were_discovered():
    """Guard against a broken discovery silently making everything below pass."""
    assert PYTHON_FILES, "no tracked Python files found"
    assert SHELL_FILES, "no tracked shell scripts found"


@pytest.mark.parametrize("path", PYTHON_FILES, ids=ids(PYTHON_FILES))
def test_python_file_compiles(path, tmp_path):
    """Every Python file must be valid syntax for the interpreter under test.

    This is a compile-only check: the modules are never imported, so CMSSW,
    ROOT and friends are not needed.
    """
    try:
        py_compile.compile(str(path), cfile=str(tmp_path / "out.pyc"), doraise=True)
    except py_compile.PyCompileError as error:
        pytest.fail(f"{path.relative_to(REPO_ROOT)} does not compile:\n{error}")


@pytest.mark.parametrize("path", SHELL_FILES, ids=ids(SHELL_FILES))
def test_shell_script_parses(path):
    """Every shell script must parse (`bash -n`), without being executed."""
    result = subprocess.run(
        ["bash", "-n", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    assert result.returncode == 0, (
        f"{path.relative_to(REPO_ROOT)} has a syntax error:\n"
        f"{result.stdout.decode(errors='replace')}"
    )


@pytest.mark.parametrize("path", JSON_FILES, ids=ids(JSON_FILES))
def test_json_file_is_valid(path):
    with path.open(encoding="utf-8") as handle:
        try:
            json.load(handle)
        except json.JSONDecodeError as error:
            pytest.fail(f"{path.relative_to(REPO_ROOT)} is not valid JSON: {error}")


@pytest.mark.parametrize("path", YAML_FILES, ids=ids(YAML_FILES))
def test_yaml_file_is_valid(path):
    yaml = pytest.importorskip("yaml", reason="PyYAML is not installed")
    with path.open(encoding="utf-8") as handle:
        try:
            list(yaml.safe_load_all(handle))
        except yaml.YAMLError as error:
            pytest.fail(f"{path.relative_to(REPO_ROOT)} is not valid YAML: {error}")


@pytest.mark.parametrize("path", REQUIREMENT_FILES, ids=ids(REQUIREMENT_FILES))
def test_requirements_are_pinned(path):
    """Plot-producing scripts must stay reproducible, so their deps are pinned."""
    unpinned = []
    for line in path.read_text(encoding="utf-8").splitlines():
        requirement = line.split("#", 1)[0].strip()
        if not requirement or requirement.startswith("-"):
            continue
        if "==" not in requirement:
            unpinned.append(requirement)
    assert not unpinned, (
        f"{path.relative_to(REPO_ROOT)} has unpinned requirements: {unpinned}"
    )


if __name__ == "__main__":
    sys.exit(pytest.main([*sys.argv[1:], str(Path(__file__))]))
