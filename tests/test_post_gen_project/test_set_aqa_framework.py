from hooks.post_gen_project import remove_folder, set_aqa_framework
from pathlib import Path
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def patch_remove_folder(mocker) -> MagicMock:
    """Patch the `remove_folder` function."""
    return mocker.patch("hooks.post_gen_project.remove_folder", side_effect=remove_folder)


# Define test cases for the `TestSetAqaFramework` test class
args_test_set_aqa_framework = ["hello", "world"]
args_test_set_aqa_framework_temporary_frameworks = [
    ("This is the request template.", "This is the AQA file."),
    ("Here is the request template.", "Here is the AQA file.")
]


@pytest.mark.parametrize("test_input_dir_cookiecutter_docs_aqa", args_test_set_aqa_framework)
@pytest.mark.parametrize("test_input_request_template, test_input_aqa",
                         args_test_set_aqa_framework_temporary_frameworks)
class TestSetAqaFramework:

    def test_remove_folder_called_once_correctly(self, temporary_frameworks: Path, patch_remove_folder: MagicMock,
                                                 test_input_dir_cookiecutter_docs_aqa: str) -> None:
        """Test the `remove_folder` function is called once correctly."""

        # Define a path to the example output folder, which is the parent of `temporary_frameworks`, and create a
        # directory with an example text file
        dir_docs_aqa = temporary_frameworks.parent.joinpath(test_input_dir_cookiecutter_docs_aqa)
        dir_docs_aqa.mkdir()
        dir_docs_aqa.joinpath("example.txt").write_text(f"New file in: `{test_input_dir_cookiecutter_docs_aqa}`")

        # Execute the `set_aqa_framework` function
        set_aqa_framework(temporary_frameworks, dir_docs_aqa)

        # Assert `remove_folder` is called once correctly, then delete the output folder for the next test execution
        patch_remove_folder.assert_called_once_with(dir_docs_aqa)

    def test_aqa_framework_folder_moved_correctly(self, temporary_frameworks: Path, test_input_request_template: str,
                                                  test_input_aqa: str,
                                                  test_input_dir_cookiecutter_docs_aqa: str) -> None:
        """Test the right AQA framework folder is moved to the correct location."""

        # Define a path to the example output folder, which is the parent of `temporary_frameworks`, and create a
        # directory with an example text file
        dir_docs_aqa = temporary_frameworks.parent.joinpath(test_input_dir_cookiecutter_docs_aqa)
        dir_docs_aqa.mkdir()
        dir_docs_aqa.joinpath("example.txt").write_text(f"New file in: `{test_input_dir_cookiecutter_docs_aqa}`")

        # Execute the `set_aqa_framework` function
        set_aqa_framework(temporary_frameworks, dir_docs_aqa)

        # Assert the correct text has been written
        assert dir_docs_aqa.joinpath("request_template.md").read_text() == test_input_request_template
        assert dir_docs_aqa.joinpath("aqa", "aqa.md").read_text() == test_input_aqa

        # Assert the `dir_framework` has been removed
        assert not temporary_frameworks.exists()
