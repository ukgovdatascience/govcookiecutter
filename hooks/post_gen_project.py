from shutil import rmtree
import os

# Define the folder path to the 'docs/aqa_frameworks' folder, and the future `docs/aqa` folder
DIR_DOCS_AQA_FRAMEWORKS = os.path.join("docs", "aqa_frameworks")
DIR_DOCS_AQA = os.path.join("docs", "aqa")

# Define the folder path to the `docs/pull_merge_request_templates` folder
DIR_REQUEST_TEMPLATES = os.path.join("docs", "pull_merge_request_templates")

# Define the folder path where pull/merge requests should exist as values in a dictionary, where the keys are the
# remote hosts
DIR_HOST_REQUEST_TEMPLATE = {
    "GitHub": [os.path.join(".github"), "pull_request_template.md"],
    "GitLab": [os.path.join(".gitlab", "merge_request_templates"), "{{ cookiecutter.project_name }}.md"]
}


def select_department_aqa_framework(user_option: str, default_option: str = "GDS") -> None:
    """Create analytical quality assurance (AQA) documents for a specific HM Government department.

    Args:
        user_option: User option that defines a HM Government departmental AQA framework to use.
        default_option: Default: GDS. Default option if `user_option` is not an existing framework.

    Returns:
        A new folder in the template called `docs/aqa` containing the selected HM Government departmental AQA framework.

    """

    # Get all the directories in `DIR_DOCS_AQA_FRAMEWORKS`
    all_folders = [d for d in os.listdir(DIR_DOCS_AQA_FRAMEWORKS) if os.path.isdir(d)]

    # Select the correct folder; use `default_option` if `user_option` is not a valid sub-folder in `all_folders`
    selected_folder = user_option if user_option in all_folders else default_option

    # Copy the relevant HM Government departmental AQA framework to the `docs/aqa` folder, using `default_option` if
    # `user_option` is not a valid sub-folder in `DIR_DOCS_AQA_FRAMEWORKS`
    os.rename(os.path.join(DIR_DOCS_AQA_FRAMEWORKS, selected_folder), DIR_DOCS_AQA)

    # Remove all framework folders now we have the correct AQA framework
    rmtree(DIR_DOCS_AQA_FRAMEWORKS)


def select_request_template(user_option: str, repository_hosting_platform: str, default_option: str = "GDS") -> None:
    """Select a pull/merge request template depending on HM Government department, and repository hosting platform.

    Args:
        user_option: User option that defines a HM Government departmental pull/merge request template to use.
        repository_hosting_platform: Repository hosting platform name. Must be one of `GitHub` or `GitLab`
        default_option: Default: GDS. Default option if user_option is not an existing pull/merge request
            template.

    Returns:
        A pull/merge request template in the correct location for the selected `repository_hosting_platform`.

    """

    # Get all Markdown files in `DIR_REQUEST_TEMPLATES`
    md_files = [os.path.splitext(f)[0] for f in os.listdir(DIR_REQUEST_TEMPLATES) if f.endswith(".md")]

    # Determine the selected file; fallback to `default_option` if `user_option` is not in `md_files`
    selected_md_file = f"{user_option if user_option in md_files else default_option}.md"

    # Create a directory for the new location
    if not os.path.isdir(DIR_HOST_REQUEST_TEMPLATE[repository_hosting_platform][0]):
        os.makedirs(DIR_HOST_REQUEST_TEMPLATE[repository_hosting_platform][0], exist_ok=True)

    # Move the `selected_md_file` to the correct location
    os.rename(os.path.join(DIR_REQUEST_TEMPLATES, selected_md_file),
              os.path.join(*DIR_HOST_REQUEST_TEMPLATE[repository_hosting_platform]))

    # Remove all pull/merge request templates now that we have the correct one
    rmtree(DIR_REQUEST_TEMPLATES)


if __name__ == "__main__":

    # Select the appropriate AQA framework
    select_department_aqa_framework("{{ cookiecutter.departmental_aqa_framework }}")

    # Select the appropriate pull/merge request template
    select_request_template("{{ cookiecutter.departmental_aqa_framework }}",
                            "{{ cookiecutter.repository_hosting_platform }}")
