import pytest
import sys
from pathlib import Path
from unittest.mock import patch
from io import StringIO
from importlib import import_module
from parser import parse_markdown_testcases

PYTHON_PROGRAM_PATH = "ex03.py"
MARKDOWN_PATH = "ch3/ex03.md"

@pytest.fixture
def run_main_function():
    def _run_with_mocked_io(program_name, input_text):
        module = import_module(program_name.replace('.py', ''))

        # Note the file requires main()
        with patch('sys.stdin', StringIO(input_text)):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                module.main()
                return mock_stdout.getvalue()
    return _run_with_mocked_io

@pytest.mark.parametrize("input_text, expected_output", 
                         parse_markdown_testcases(Path(__file__).parent / MARKDOWN_PATH))
def test_exercise_output(run_main_function, input_text, expected_output):
    program_to_test = PYTHON_PROGRAM_PATH # changethis
    actual_output = run_main_function(program_to_test, input_text)
    assert actual_output.strip() == expected_output.strip()