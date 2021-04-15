# `{{ cookiecutter.repo_name }}` structure

This page provides information on the repository's structure.

```{contents}
:local:
:depth: 2
```

## Folder structure

The repository's folder structure is explained here:

```{toctree}
:maxdepth: 2
./data.md
./docs.md
./notebooks.md
./outputs.md
./src.md
./tests.md
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

a code coverage report in HTML will be produced on the code in the `src` folder. This HTML report can be accessed at
`htmlcov/index.html`.

### `.envrc`

A file containing environment variables for the Git repository that can be selectively loaded. This uses the
[`direnv`][direnv] shell extension; see their documentation for further information.

This file contains a `sed` command to output a `.env` file with all the environment variables. This may be useful for
sourcing environment variables, for example in conjunction with PyCharm's EnvFile plugin.

To ensure this `sed` command works correctly, make sure any file paths listed in this file, and the
[`.secrets`](#secrets) are absolute file paths (recommended), or relative file paths using other environment variables
(works for Python users only). Environment variable names can only contain letters, numbers or underscores as well. For
example:

```shell
export DIR_DATA=$(pwd)/data  # fine for Python and R users
export DIR_DATA_EXTERNAL=$(pwd)/data/external  # fine for Python and R users
export DIR_DATA_EXTERNAL=./data/external  # fine for Python and R users
export DIR_DATA_EXTERNAL=$DIR_DATA/external  # fine for Python users only
export DIR-DATA-EXTERNAL=$DIR_DATA/external  # will break the `sed` command!
```

### `.flake8`

A configuration file for the [`flake8`][flake8] Python package that provides linting. This file is based on the
[common configuration][gds-way-flake8] described on [The GDS Way][gds-way].

### `.gitignore`

A `.gitignore` file to ignore certain files and folders from this Git repository. See the
[contributor guide][docs-updating-gitignore] for further information about modifying this file.

### `.pre-commit-config.yaml`

A pre-commit hook configuration file. See the [contributor guide][docs-pre-commit-hooks] for further details.

### `.secrets`

A file to store all secrets and credentials as environment variables. This is read-in by [`.envrc`](#envrc) using the
[`direnv`][direnv] shell extension, but is **not** tracked by Git.

### `.secrets.baseline`

Baseline file for the [`detect-secrets`][detect-secrets] package; this package detects secrets, and, in conjunction
with `pre-commit`, prevents them from being committed to the repository. The baseline file flags secret-like data that
the user deliberately wishes to commit the to repository.

### `CODE_OF_CONDUCT.md`

The [Code of Conduct][code-of-conduct] for contributors to this project, including maintainers and
`{{ cookiecutter.organisation_name }}` organisation owners.

### `conftest.py`

File to contain shared fixture functions for the [pytest][pytest] tests in the `tests` folder.

### `CONTRIBUTING.md`

The [contributing guidelines][contributing] for this project.

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
[`tests`][docs-tests] folder, execute the following command:

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

### `DESCRIPTION`
R-specific. Information related to the project including the name, authors and packages necessary for the project.

### `startup.R`
R-specific. Installs necessary packages specified in the `DESCRIPTION` file upon starting R via `.Rprofile`.

### `.Rprofile`
R-specific. Initialisation file that runs automatically when starting R.

### `.lintr`
R-specific. Configuration file for styling R code that's used by pre-commit hooks to check R code.


[code-of-conduct]:../contributor_guide/CODE_OF_CONDUCT.md
[contributing]: ../contributor_guide/CONTRIBUTING.md
[coverage]: https://coverage.readthedocs.io/
[detect-secrets]: https://github.com/Yelp/detect-secrets
[direnv]: https://direnv.net/
[docs-pre-commit-hooks]: ../contributor_guide/pre_commit_hooks.md
[docs-tests]: ./tests.md
[docs-updating-gitignore]: ../contributor_guide/updating_gitignore.md
[flake8]: https://gitlab.com/pycqa/flake8
[gds-way]: https://gds-way.cloudapps.digital
[gds-way-flake8]: https://gds-way.cloudapps.digital/manuals/programming-languages/python/python.html#common-configuration
[pytest]: https://docs.pytest.org/
