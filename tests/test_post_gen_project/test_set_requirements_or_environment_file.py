from hooks.post_gen_project import set_requirements_or_environment_file
from pathlib import Path
import pytest


@pytest.fixture
def make_temporary_directory(tmp_path_factory, test_input_requirements: str, test_input_environment: str) -> Path:
    """Make a temporary directory, and add a `requirements.txt` and an `environment.yml` file."""

    # Create a temporary directory
    dir_path = tmp_path_factory.mktemp("temporary_dir", True)

    # Create a `requirements.txt`, and `environment.yml` file, populating them with text; return `dir_path`
    dir_path.joinpath("requirements.txt").write_text(test_input_requirements)
    dir_path.joinpath("environment.yml").write_text(test_input_environment)
    return dir_path


# Define test cases for the `TestSetRequirementsOrEnvironmentFile` test class
args_requirements_environment_text = [
    ("This is a `requirements.txt` file!", "This is an `environment.yml` file!"),
    ("Here is a `requirements.txt` file!", "Here is an `environment.yml` file!")
]
args_invalid_package_manager_names = ["pip+conda", "hello", "world"]


@pytest.mark.parametrize("test_input_requirements, test_input_environment", args_requirements_environment_text)
class TestSetRequirementsOrEnvironmentFile:

    def test_function_operates_correctly_for_pip_package_manager(self, make_temporary_directory: Path,
                                                                 test_input_requirements: str) -> None:
        """Test that the function operates correct if `pip` is the selected package manager."""

        # Execute the `set_requirements_or_environment_file` function assuming `pip` is the selected package manager
        set_requirements_or_environment_file("pip", make_temporary_directory.joinpath("requirements.txt"),
                                             make_temporary_directory.joinpath("environment.yml"))

        # Assert that the `requirements.txt` file still exists, but the `environment.yml` file has been deleted
        assert make_temporary_directory.joinpath("requirements.txt").exists()
        assert not make_temporary_directory.joinpath("environment.yml").exists()

        # Assert the text in `requirements.txt` is correct
        assert make_temporary_directory.joinpath("requirements.txt").read_text() == test_input_requirements

    def test_function_operates_correctly_for_conda_package_manager(self, make_temporary_directory: Path,
                                                                   test_input_environment: str) -> None:
        """Test that the function operates correct if `conda` is the selected package manager."""

        # Execute the `set_requirements_or_environment_file` function assuming `conda` is the selected package manager
        set_requirements_or_environment_file("conda", make_temporary_directory.joinpath("requirements.txt"),
                                             make_temporary_directory.joinpath("environment.yml"))

        # Assert that the `environment.yml` file still exists, but the `requirements.txt` file has been deleted
        assert make_temporary_directory.joinpath("environment.yml").exists()
        assert not make_temporary_directory.joinpath("requirements.txt").exists()

        # Assert the text in `environment.yml` is correct
        assert make_temporary_directory.joinpath("environment.yml").read_text() == test_input_environment

    @pytest.mark.parametrize("test_input_test_manager_invalid", args_invalid_package_manager_names)
    def test_function_raises_valueerror_if_not_pip_or_conda(self, make_temporary_directory: Path,
                                                            test_input_test_manager_invalid: str) -> None:
        """Test that the function raises a `ValueError` if neither `pip` or `conda` is the selected package manager."""

        # Execute the `set_requirements_or_environment_file` function assuming `conda` is the selected package manager;
        # check this raises a `ValueError`
        with pytest.raises(ValueError):
            set_requirements_or_environment_file(test_input_test_manager_invalid,
                                                 make_temporary_directory.joinpath("requirements.txt"),
                                                 make_temporary_directory.joinpath("environment.yml"))
