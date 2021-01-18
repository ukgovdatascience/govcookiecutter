from hooks.post_gen_project import remove_folder
from pathlib import Path
from typing import List
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def patch_rmtree(mocker) -> MagicMock:
    """Patch the `rmtree` function."""
    return mocker.patch("hooks.post_gen_project.rmtree")


@pytest.fixture
def make_temporary_directories(tmp_path_factory, test_input_directory_names: List[str]) -> Path:
    """Make a range of temporary directories."""

    # Create a temporary directory, and populate it with directors. Return the temporary directory path
    dir_path = tmp_path_factory.mktemp("temporary_dir", True)
    _ = [dir_path.joinpath(d).mkdir() for d in test_input_directory_names]
    return dir_path


# Define test cases for the `TestRemoveFolder.test_operates_correctly` test class method
args_test_remove_folder_operates_correctly = [
    (["a", "b"], "a"),
    (["a", "b", "c"], "c"),
    (["a", "b", "c", "d"], "b"),
]


class TestRemoveFolder:

    @pytest.mark.parametrize("test_input_folder", ["hello", "world"])
    def test_rmtree_called_once_correctly(self, patch_rmtree: MagicMock, test_input_folder: str) -> None:
        """Test the `rmtree` function is called once correctly."""

        # Execute the `remove_folder` function, and assert `rmtree` is called once correctly
        remove_folder(test_input_folder)
        patch_rmtree.assert_called_once_with(test_input_folder)

    @pytest.mark.parametrize("test_input_directory_names, test_input_remove_directory",
                             args_test_remove_folder_operates_correctly)
    def test_operates_correctly(self, make_temporary_directories: Path, test_input_directory_names: List[str],
                                test_input_remove_directory: str) -> None:
        """Test the function operates correctly, and removes a folder."""

        # Remove the `test_input_remove_directory` folder
        remove_folder(make_temporary_directories.joinpath(test_input_remove_directory))

        # Assert that all folders except `test_input_remove_directory` exist
        for test_input_directory_name in test_input_directory_names:
            if test_input_directory_name == test_input_remove_directory:
                assert not make_temporary_directories.joinpath(test_input_directory_name).exists()
            else:
                assert make_temporary_directories.joinpath(test_input_directory_name).exists()
