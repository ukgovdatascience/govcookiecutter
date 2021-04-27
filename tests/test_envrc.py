from pathlib import Path
from typing import Dict, List

# Define a path to the `govcookiecutter` template directory, and its `.envrc` file
DIR_TEMPLATE = Path("{{ cookiecutter.repo_name }}")
PATH_TEMPLATE_ENVRC = DIR_TEMPLATE.joinpath(".envrc")

# Define a list of directory names to recursively ignore, as well as a list of directory names to ignore at the
# root-level of the `govcookiecutter` template directory, and a list of dictionary names to ignore in certain
# root-level directories
EXCLUDE_DIR_NAMES = ["__pycache__"]
EXCLUDE_ROOT_DIR_NAMES = [*EXCLUDE_DIR_NAMES, ".govcookiecutter"]
EXCLUDE_SUB_DIR_IN_PARENTS_NAMES = [*EXCLUDE_ROOT_DIR_NAMES, "docs"]


def get_actual_envrc_variables(path_envrc: Path) -> Dict[str, Path]:
    """Get the export variables and values for directories in the `.envrc` file of the `govcookiecutter` template.

    Args:
        path_envrc: A file path to the `.envrc` file of the `govcookiecutter` template.

    Returns:
        A dictionary where the keys are the names of the export directory variables, and the values are the export
        directory values.

    """

    # Instantiate a saving dictionary variable
    envrc_actual_dir_variable = {}

    # Open the `path_envrc` file, and get all export variables starting with `DIR`, and the values assigned to them,
    # and return the output
    with path_envrc.open() as f:
        for line in f.readlines():
            if line.startswith("export DIR"):
                k, v = line.lstrip("export ").strip().replace("$(pwd)", path_envrc.parent.name).split("=")
                envrc_actual_dir_variable[k] = Path(v)
    return envrc_actual_dir_variable


def define_expected_envrc_variables(folder: Path, exclude_folders: List[str], exclude_root_folders: List[str],
                                    exclude_sub_folders_in_parent_folders: List[str]) -> Dict[str, Path]:
    """Get the expected export directory variables and values in the `.envrc` file of the `govcookiecutter` template.

    Args:
        folder: A folder path to the `govcookiecutter` template folder.
        exclude_folders: A list of folder names to ignore when encountered.
        exclude_root_folders: A list of root-level folder names in `folder` to ignore.
        exclude_sub_folders_in_parent_folders: A list of folder names at the root-level of `folder` where their
            sub-folders should be ignored.

    Returns:
        A dictionary where the keys are expected export directory variables, and the values are the expected export
        directory values of the `.envrc` file in the `govcookiecutter` template directory `folder`.

    """

    # Get the names of all root-level directories in `folder`, where each name is in upper case in the format
    # "DIR_<<<DIRECTORY_NAME>>>". Ignore any directories with a name in `exclude_root_folders`
    envrc_expected_dir_variable = {
        f"DIR_{d.name.upper()}": d for d in folder.glob("*") if d.is_dir() and d.name not in exclude_root_folders
    }

    # Get all sub-directory names one-level down from `folder`, where the directory name is not in `exclude_folders`,
    # and the parent directory name is not in `exclude_sub_folders_in_parent_folders`. Each name is in upper case in
    # the format "DIR_<<<PARENT_DIRECTORY_NAME>>>_<<<DIRECTORY_NAME>>>". Return `envrc_expected_dir_variable`
    for d in folder.glob("*/*"):
        if d.is_dir() and d.name not in exclude_folders and d.parent.name not in exclude_sub_folders_in_parent_folders:
            envrc_expected_dir_variable[f"DIR_{d.parent.name.upper()}_{d.name.upper()}"] = d
    return envrc_expected_dir_variable


class TestEnvrcExportDirectories:

    def test_values_are_directories(self) -> None:
        """Test that the export values are real dictionaries."""
        for n, d in get_actual_envrc_variables(PATH_TEMPLATE_ENVRC).items():
            assert d.is_dir(), f"`{n}` variable directory does not exist: {d}"

    def test_variables_as_expected(self) -> None:
        """Test that the export directory variable and value names in `.envrc` are as expected."""

        # Get the expected `.envrc` directory variables, and assert the actual variables are as expected
        test_expected = define_expected_envrc_variables(DIR_TEMPLATE, EXCLUDE_DIR_NAMES, EXCLUDE_ROOT_DIR_NAMES,
                                                        EXCLUDE_SUB_DIR_IN_PARENTS_NAMES)
        assert get_actual_envrc_variables(PATH_TEMPLATE_ENVRC) == test_expected
