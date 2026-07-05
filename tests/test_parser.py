"""Unit tests for the response parser."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.parser import extract_actions, extract_plan, has_actions, WriteAction, DeleteAction

SAMPLE_RESPONSE = """
Here's what I'll do.

PLAN:
  WRITE  src/app.py
  EDIT   requirements.txt
  DELETE src/old.py

<<<FILE: src/app.py
def main():
    print("hello world")

if __name__ == "__main__":
    main()
>>>

<<<FILE: requirements.txt
flask==3.0.0
>>>

<<<DELETE: src/old.py>>>
"""


def test_extract_actions_finds_writes():
    actions = extract_actions(SAMPLE_RESPONSE)
    writes = [a for a in actions if isinstance(a, WriteAction)]
    assert len(writes) == 2
    paths = {a.path for a in writes}
    assert "src/app.py" in paths
    assert "requirements.txt" in paths


def test_extract_actions_finds_deletes():
    actions = extract_actions(SAMPLE_RESPONSE)
    deletes = [a for a in actions if isinstance(a, DeleteAction)]
    assert len(deletes) == 1
    assert deletes[0].path == "src/old.py"


def test_file_content_is_correct():
    actions = extract_actions(SAMPLE_RESPONSE)
    writes = [a for a in actions if isinstance(a, WriteAction)]
    app_py = next(a for a in writes if a.path == "src/app.py")
    assert "def main():" in app_py.content
    assert "hello world" in app_py.content


def test_extract_plan():
    plan = extract_plan(SAMPLE_RESPONSE)
    assert plan is not None
    assert "WRITE" in plan
    assert "EDIT" in plan
    assert "DELETE" in plan


def test_has_actions_true():
    assert has_actions(SAMPLE_RESPONSE) is True


def test_has_actions_false():
    assert has_actions("Just a plain text response with no files.") is False


def test_no_actions_plain_response():
    actions = extract_actions("Just answering a question here.")
    assert len(actions) == 0


def test_action_order():
    """Actions should come out in document order."""
    actions = extract_actions(SAMPLE_RESPONSE)
    # First two are writes (app.py, requirements.txt), then a delete
    assert isinstance(actions[0], WriteAction)
    assert isinstance(actions[1], WriteAction)
    assert isinstance(actions[2], DeleteAction)


if __name__ == "__main__":
    tests = [
        test_extract_actions_finds_writes,
        test_extract_actions_finds_deletes,
        test_file_content_is_correct,
        test_extract_plan,
        test_has_actions_true,
        test_has_actions_false,
        test_no_actions_plain_response,
        test_action_order,
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
            print(f"  ERROR {t.__name__}  —  {e}")

    print(f"\n{passed}/{len(tests)} tests passed.")
