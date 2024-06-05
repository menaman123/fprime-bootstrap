import os
import sys
import subprocess
import tempfile
from pathlib import Path
import pytest

# Define the command to run the fprime-bootstrap tool
COMMAND = [sys.executable, "-m", "fprime_bootstrap", "project", "--path"]

@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

def run_fprime_bootstrap(temp_dir):
    """Run fprime-bootstrap in the temporary directory."""
    result = subprocess.run(COMMAND + [temp_dir], capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    return result

def test_no_template_files(temp_directory):
    """Test that no files are named *-template."""
    temp_dir = temp_directory
    result = run_fprime_bootstrap(temp_dir)
    
    # Check that the command executed successfully
    assert result.returncode == 0, f"fprime-bootstrap failed: {result.stderr}"

    # Check that no files are named *-template
    for root, _, files in os.walk(temp_dir):
        for file in files:
            assert not file.endswith("-template"), f"Template file found: {file}"

def test_no_placeholder_strings(temp_directory):
    """Test that no files contain the placeholder string {{FPRIME_PROJECT_NAME}}."""
    temp_dir = temp_directory
    result = run_fprime_bootstrap(temp_dir)
    
    # Check that the command executed successfully
    assert result.returncode == 0, f"fprime-bootstrap failed: {result.stderr}"

    # Check that no files contain the string {{FPRIME_PROJECT_NAME}}
    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = Path(root) / file
            with open(file_path, "r") as f:
                contents = f.read()
                assert "{{FPRIME_PROJECT_NAME}}" not in contents, f"Placeholder string found in {file_path}"

if __name__ == "__main__":
    pytest.main()
