from hooks.post_gen_project import set_request_template
from pathlib import Path
import pytest


# Define test cases for the `TestSetRequestTemplate` test class
args_test_set_request_template_valueerror_for_bad_repository_hosting_platform = ["hello", "world"]
args_test_set_request_template_request_template_moved_correctly = ["Github", "gitlab", "GITHUB", "gitLab"]
args_test_set_request_template_temporary_frameworks = [
    ("This is the request template.", "This is the AQA file."),
    ("Here is the request template.", "Here is the AQA file.")
]


@pytest.mark.parametrize("test_input_request_template, test_input_aqa",
                         args_test_set_request_template_temporary_frameworks)
class TestSetRequestTemplate:

    @pytest.mark.parametrize("test_input_repository_hosting_platform",
                             args_test_set_request_template_valueerror_for_bad_repository_hosting_platform)
    def test_valueerror_for_bad_repository_hosting_platform(self, temporary_frameworks: Path,
                                                            test_input_repository_hosting_platform: str) -> None:
        """Test a `ValueError` is raised if the repository hosting platform is not Github or GitLab."""
        with pytest.raises(ValueError):
            set_request_template(temporary_frameworks.joinpath("request_template.md"), temporary_frameworks.parent,
                                 test_input_repository_hosting_platform)

    @pytest.mark.parametrize("test_input_repository_hosting_platform",
                             args_test_set_request_template_request_template_moved_correctly)
    def test_request_template_moved_correctly(self, temporary_frameworks: Path, test_input_request_template: str,
                                              test_input_repository_hosting_platform: str) -> None:
        """Test the right AQA framework folder is moved to the correct location."""

        # Execute the `set_request_template` function
        set_request_template(temporary_frameworks.joinpath("request_template.md"), temporary_frameworks.parent,
                             test_input_repository_hosting_platform)

        # Assert the correct text has been written to the correct location
        if test_input_repository_hosting_platform.lower() == "github":
            test_output = temporary_frameworks.parent.joinpath(".github", "pull_request_template.md").read_text()
        else:
            test_output = temporary_frameworks.parent.joinpath(".gitlab", "merge_request_templates",
                                                               "{{ cookiecutter.project_name }}.md").read_text()
        assert test_output == test_input_request_template
