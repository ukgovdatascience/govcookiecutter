# `govcookiecutter` structure

This page provides information on the repository's structure.

```{contents}
:local:
:depth: 2
```

## Folder structure

The repository's folder structure is explained here:

```{toctree}
:maxdepth: 2
./docs.md
./example.md
./hooks.md
./tests.md
./{{ cookiecutter.repo_name }}.md
```

## Top-level files

Each subsection here contains a brief description about the files at the top-level of this Git repository.

### `.coveragerc`

A file containing configuration settings for the [`coverage`][coverage] Python package. When executed with
[`pytest`][pytest] using the following command:

```shell
coverage run -m pytest
coverage html
```

a code coverage report in HTML will be produced on the code in the [hooks][docs-hooks], and
`{{ cookiecutter.repo_name }}/src` folders. This HTML report can be accessed at `htmlcov/index.html`.

### `.flake8`

A configuration file for the [`flake8`][flake8] Python package that provides linting. This file is based on the
[common configuration][gds-way-flake8] described on [The GDS Way][gds-way].

### `.gitignore`

A `.gitignore` file to ignore certain files and folders from this Git repository. See the
[contributor guide][docs-updating-gitignore] for further information about modifying this file.

### `.pre-commit-config.yaml`

A pre-commit hook configuration file. See the [contributor guide][docs-pre-commit-hooks] for further details.

### `.secrets.baseline`

Baseline file for the [`detect-secrets`][detect-secrets] package; this package detects secrets, and, in conjunction
with `pre-commit`, prevents them from being committed to the repository. The baseline file flags secret-like data that
the user deliberately wishes to commit to the repository.

### `CODE_OF_CONDUCT.md`

The [Code of Conduct][code-of-conduct] for contributors to this project, including maintainers and `ukgovdatascience`
organisation owners.

### `conftest.py`

File to contain shared fixture functions for the [pytest][pytest] tests in the `tests` folder.

### `CONTRIBUTING.md`

The [contributing guidelines][contributing] for this project.

### `cookiecutter.json`

A JSON file containing the prompts and default values during template generation. Note any keys beginning with an
underscore are not shown to users. The first block of JSON refers to cookiecutter extensions. The next block relates to
departmental-specific information, such as your public sector department, and its organisation handle on GitHub or
GitLab. The last block relates to project-specific information.

For further information, see the [cookiecutter][cookiecutter] package documentation.

### `LICENSE`

The licence for this project. Unless stated otherwise, the codebase is released under the MIT License. This covers both
the codebase and any sample code in the documentation. The documentation is © Crown copyright and available under the
terms of the Open Government 3.0 licence.

### `Makefile`

The `Makefile` contains a set of commands for the `make` utility. Run the `help` command for further information at the
top-level of the Git repository.

```shell
make help
```

### `pytest.ini`

A file containing configuration settings for the [`pytest`][pytest] Python package. To run tests within the
[`tests`][docs-tests], and `{{ cookiecutter.repo_name }}/tests` folders, execute the following
command:

```shell
pytest
```

### `README.md`

An overview of the Git repository, including all necessary instructions to execute the code.

### `requirements.txt`

A list of Python package requirements for this Git repository, which can be installed using the `pip install` command.

```shell
pip install --requirement requirements.txt
```

Alternatively, to install the requirements file along with pre-commit hooks, run the following command:

```shell
make requirements
```

[code-of-conduct]: ../guides/CODE_OF_CONDUCT.md
[contributing]: ../guides/CONTRIBUTING.md
[cookiecutter]: https://cookiecutter.readthedocs.io/
[coverage]: https://coverage.readthedocs.io/
[detect-secrets]: https://github.com/Yelp/detect-secrets
[direnv]: https://direnv.net/
[docs-hooks]: ./hooks.md
[docs-pre-commit-hooks]: ../guides/%7B%7B%20cookiecutter.repo_name%20%7D%7D/docs/contributor_guide/pre_commit_hooks.md
[docs-tests]: ./tests.md
[docs-updating-gitignore]: ../guides/%7B%7B%20cookiecutter.repo_name%20%7D%7D/docs/contributor_guide/updating_gitignore.md
[flake8]: https://gitlab.com/pycqa/flake8
[gds-way]: https://gds-way.cloudapps.digital
[gds-way-flake8]: https://gds-way.cloudapps.digital/manuals/programming-languages/python/python.html#common-configuration
[pytest]: https://docs.pytest.org/
