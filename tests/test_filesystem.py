"""Unit tests for safe file system operations."""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.filesystem import write_file, delete_file, read_file, FileSystemError


def setup_project():
    """Create a temp project dir and return its path."""
    return tempfile.mkdtemp(prefix="kiro_test_")


def teardown_project(path):
    shutil.rmtree(path, ignore_errors=True)


def test_write_creates_file():
    proj = setup_project()
    try:
        write_file(proj, "hello.txt", "hello world\n")
        assert os.path.exists(os.path.join(proj, "hello.txt"))
    finally:
        teardown_project(proj)


def test_write_creates_subdirs():
    proj = setup_project()
    try:
        write_file(proj, "src/utils/helpers.py", "# helpers\n")
        assert os.path.exists(os.path.join(proj, "src", "utils", "helpers.py"))
    finally:
        teardown_project(proj)


def test_write_creates_backup():
    proj = setup_project()
    try:
        write_file(proj, "app.py", "v1\n")
        write_file(proj, "app.py", "v2\n")
        bak = os.path.join(proj, "app.py.bak")
        assert os.path.exists(bak)
        with open(bak) as f:
            assert f.read() == "v1\n"
    finally:
        teardown_project(proj)


def test_read_file():
    proj = setup_project()
    try:
        write_file(proj, "notes.txt", "hello\n")
        content = read_file(proj, "notes.txt")
        assert content == "hello\n"
    finally:
        teardown_project(proj)


def test_delete_file():
    proj = setup_project()
    try:
        write_file(proj, "tmp.txt", "bye\n")
        delete_file(proj, "tmp.txt")
        assert not os.path.exists(os.path.join(proj, "tmp.txt"))
    finally:
        teardown_project(proj)


def test_delete_nonexistent_raises():
    proj = setup_project()
    try:
        try:
            delete_file(proj, "ghost.txt")
            assert False, "Should have raised FileSystemError"
        except FileSystemError:
            pass
    finally:
        teardown_project(proj)


def test_path_traversal_blocked():
    proj = setup_project()
    try:
        try:
            write_file(proj, "../escape.txt", "bad\n")
            assert False, "Should have raised FileSystemError"
        except FileSystemError as e:
            assert "traversal" in str(e).lower()
    finally:
        teardown_project(proj)


if __name__ == "__main__":
    tests = [
        test_write_creates_file,
        test_write_creates_subdirs,
        test_write_creates_backup,
        test_read_file,
        test_delete_file,
        test_delete_nonexistent_raises,
        test_path_traversal_blocked,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}  —  {e}")
        except Exception as e:
            print(f"  ERROR {t.__name__}  —  {type(e).__name__}: {e}")

    print(f"\n{passed}/{len(tests)} tests passed.")
