from pathlib import Path
import pytest


@pytest.fixture
def temporary_frameworks(tmp_path, test_input_request_template: str, test_input_aqa: str, ) -> Path:
    """Create a temporary frameworks folder with sub-folders, and files."""

    # Create a temporary folder
    dir_example = tmp_path.joinpath("example")

    # Create a temporary frameworks folder, and add an `aqa` folder
    dir_framework = dir_example.joinpath("test_framework")
    dir_framework.joinpath("aqa").mkdir(parents=True)

    # Add text Markdown files in `dir_framework`, and its `aqa` folder
    dir_framework.joinpath("request_template.md").write_text(test_input_request_template)
    dir_framework.joinpath("aqa", "aqa.md").write_text(test_input_aqa)

    # Return the path to the temporary frameworks folder
    return dir_framework
