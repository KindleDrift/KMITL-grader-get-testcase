import pytest
import sys
from pathlib import Path
from unittest.mock import patch
from io import StringIO
from importlib import import_module
import importlib.util
from parser import parse_markdown_testcases
from dotenv import load_dotenv
import os

load_dotenv()

PYTHON_PROGRAM_PATH = Path(os.getenv("PYTHON_PROGRAM_PATH"))
MARKDOWN_PATH = Path(os.getenv("MARKDOWN_PATH"))

program_dir = Path(__file__).parent.parent.parent / PYTHON_PROGRAM_PATH
sys.path.append(str(program_dir.resolve().parent))

@pytest.fixture
def run_main_function():
    def _run_with_mocked_io(program_path_str, input_text):
        module_name = program_path_str.split(os.sep)[-1].replace('.py', '')
        module = import_module(module_name)
        
        with patch('sys.stdin', StringIO(input_text)):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                module.main()
                return mock_stdout.getvalue()
    return _run_with_mocked_io


@pytest.mark.parametrize("input_text, expected_output", 
                         parse_markdown_testcases(Path(__file__).parent.parent / MARKDOWN_PATH))
def test_exercise_output(run_main_function, input_text, expected_output):
    program_to_test = str(program_dir)
    actual_output = run_main_function(program_to_test, input_text)
    assert actual_output.strip() == expected_output.strip()

