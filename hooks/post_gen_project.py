from pathlib import Path
from shutil import rmtree
from typing import Union


def remove_folder(folder: Union[Path, str]) -> None:
    """Remove a folder.

    Args:
        folder: A folder path to be removed.

    Returns:
        None - removes the `folder` folder.

    """
    rmtree(folder)


def set_aqa_framework(dir_department_framework_aqa: Union[Path, str],
                      dir_cookiecutter_docs_aqa: Union[Path, str]) -> None:
    """Set a specific HM Government department analytical quality assurance (AQA) framework.

    Args:
        dir_department_framework_aqa: A folder path that contains a specific HM Government department AQA framework.
        dir_cookiecutter_docs_aqa: A folder path within the outputted project structure, where the contents of
            `dir_department_framework_aqa` will reside.

    Returns:
        The department-specific AQA framework in the outputted project structure's `dir_cookiecutter_docs_aqa` folder.

    """

    # Remove the default `docs/aqa` folder, and its contents. Then recursively create a new folder path to here
    remove_folder(dir_cookiecutter_docs_aqa)

    # Copy the relevant HM Government departmental AQA framework to the `docs/aqa` folder
    _ = Path(dir_department_framework_aqa).rename(dir_cookiecutter_docs_aqa)


def set_request_template(path_department_framework_request_template: Union[Path, str],
                         dir_govcookiecutter: Union[Path, str], repository_hosting_platform: str) -> None:
    """Set a pull or merge request template in the outputted project structure for a specific HM Government department.

    A pull request template is created if the user chooses GitHub as their repository hosting platform. A merge request
    template is created if they choose GitLab instead.

    Args:
        path_department_framework_request_template: A file path to the specific HM Government department pull or merge
            request template.
        dir_govcookiecutter: A folder path to the outputted `govcookiecutter` template.
        repository_hosting_platform: The repository hosting platform. Must be one of "GitHub" or "GitLab" (case
            insensitive).

    Returns:
        A department-specific pull or merge request template in the correct location, depending on their choice of
        GitHub or GitLab as the repository hosting platform. If neither GitHub or GitLab are chosen, a `ValueError` is
        raised.

    """

    # Define the file path where the request template will be moved, which is dependent on the repository hosting
    # platform. If the `dir_request_template` is not initially one of `.github` or `.gitlab`, raise a `ValueError`
    if repository_hosting_platform.lower() == "github":
        path_request_template = Path(dir_govcookiecutter).joinpath(f".{repository_hosting_platform.lower()}",
                                                                   "pull_request_template.md")
    elif repository_hosting_platform.lower() == "gitlab":
        path_request_template = Path(dir_govcookiecutter).joinpath(f".{repository_hosting_platform.lower()}",
                                                                   "merge_request_templates",
                                                                   "{{ cookiecutter.project_name }}.md")
    else:
        raise ValueError("`repository_hosting_platform` must be one of `GitHub` or `GitLab`: "
                         f"{repository_hosting_platform}")

    # Recursively create all the directories to the parent directory of `path_request_template` if they do not already
    # exist
    if not path_request_template.parent.is_dir():
        path_request_template.parent.mkdir(parents=True, exist_ok=True)

    # Move the `path_department_framework_request_template` to `path_request_template`
    _ = Path(path_department_framework_request_template).rename(path_request_template)


if __name__ == "__main__":

    # Define the folder path to `.govcookiecutter`
    DIR_GOVCOOKIECUTTER = Path(".govcookiecutter")

    # Check `{{ cookiecutter.departmental_framework }}` is not `N/A`
    if "{{ cookiecutter.departmental_framework }}" != "N/A":

        # Define the folder path to the specific department framework of interest in the `department_frameworks` folder
        DIR_DEPARTMENT_FRAMEWORKS = DIR_GOVCOOKIECUTTER.joinpath("department_frameworks",
                                                                 "{{ cookiecutter.departmental_framework }}")

        # Transfer the `aqa` folder, and the pull/merge request templates to the correct folder paths
        set_aqa_framework(DIR_DEPARTMENT_FRAMEWORKS.joinpath("aqa"), Path("docs").joinpath("aqa"))
        set_request_template(DIR_DEPARTMENT_FRAMEWORKS.joinpath("request_template.md"), Path.cwd(),
                             "{{ cookiecutter.repository_hosting_platform }}")

    # Remove `DIR_GOVCOOKIECUTTER`
    remove_folder(DIR_GOVCOOKIECUTTER)
