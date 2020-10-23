# Project structure

```eval_rst
.. contents::
    :local:
    :depth: 2

```

## Folder structure

Each subsection here contains a brief description about the suggested usage of these folders.

### `data` folder

Any data that needs to be stored locally should be saved in this location. This folder, and all its sub-folders are not
version-controlled.

The sub-folders should be used as follows:

- `external`: Any data that will **not** be processed at all, such as reference data;
- `raw`: Any raw data before any processing;
- `interim`: Any raw data that has been partially processed and, for whatever reason, needs to be stored before further
processing is completed; and
- `processed`: Any raw or interim data that has been fully processed into its final state.

The folder paths for these directories are loaded as environment variables by the [`.envrc`](#envrc) file; to load them
in Python, use any or all of the following code:

```python
import os

DIR_DATA = os.environ.get("DIR_DATA")
DIR_DATA_EXTERNAL = os.environ.get("DIR_DATA_EXTERNAL")
DIR_DATA_RAW = os.environ.get("DIR_DATA_RAW")
DIR_DATA_INTERIM = os.environ.get("DIR_DATA_INTERIM")
DIR_DATA_PROCESSED = os.environ.get("DIR_DATA_PROCESSED")
```

### `docs` folder

All documentation for the project should be included in this folder in either Markdown or ReStructuredText files, with
acceptable formatting for Sphinx.

To build the documentation, run the `docs` command from the [`Makefile`](#makefile) using the `make` utility at the
top-level of this Git repository.

```
make docs
```

For further information about writing Sphinx documentation, see the `README.md` file in the `docs` folder.

#### Analytical quality assurance (AQA)

All analytical quality assurance (AQA) documents can be found in the `docs/aqa` folder. These files document how this
project meets HM Government guidance on producing quality analysis, as described in the
[Aqua book](https://www.gov.uk/government/publications/the-aqua-book-guidance-on-producing-quality-analysis-for-government).

### `notebooks` folder

All Jupyter notebooks should be stored in this folder. The [`.envrc`](#envrc) file should automatically add the entire
project path into the `PYTHONPATH` environment variable - this should allow you to directly import `src` in your
notebook.

### `outputs` folder

All outputs from the project should be stored here. This folder path for these directories is loaded as an environment
variable by the [`.envrc`](#envrc) file; to load them in Python, use the following code:

```python
import os

DIR_OUTPUT = os.environ.get("DIR_OUTPUT")
```

### `src` package

All functions for this project, should be stored in this folder. **All tests should be stored in the
[`tests`](#tests-folder) folder**, which is one-level above this folder in the main project directory.

The sub-folders should be used as follows:

- `make_data`: Data processing-related functions;
- `make_features`: Feature-related functions, for example, functions to create features from processed data;
- `make_models`: Model-related functions;
- `make_visualisations`: Functions to produce visualisations;
- `utils`: Utility functions that are helpful in the project.

Feel free to create/rename/delete these folders as required, as they will not be necessary for each and every project.

It is strongly suggested that you import functions in the `src` `__init__.py` script. You should also
try and use absolute imports in this script whenever possible; relative imports are not discouraged, but can be an
issue for projects where the directory structure is likely to change. See
[PEP 328](https://www.python.org/dev/peps/pep-0328/) for further information.

### `tests` folder

All tests for the functions defined in the [`src`](#src-package) package should be stored here.

## Top-level files

Each subsection here contains a brief description about the files at the top-level of this Git repository.

### `.envrc`

A file containing environment variables for the Git repository that can be selectively loaded. This uses the
[`direnv`](https://direnv.net/) shell extension; see their documentation for further information.

### `.flake8`

A configuration file for the [`flake8`](https://gitlab.com/pycqa/flake8) Python package that provides linting. This
file is based on the
[common configuration](https://gds-way.cloudapps.digital/manuals/programming-languages/python/python.html#common-configuration)
described on [The GDS Way](https://gds-way.cloudapps.digital).

### `.gitignore`

A `.gitignore` file to ignore certain files and folders from this Git repository. See the
[GitHub Help pages](https://help.github.com/en/github/using-git/ignoring-files) for further information.

### `.pre-commit-config.yaml`

A pre-commit hook configuration file. See the `pre-commit` package [documentation](https://pre-commit.com/) for further
details.
{% if cookiecutter.create_secrets_file == "Yes" %}
### `.secrets`

A file to store all secrets and credentials as environment variables. This is read-in by [`.envrc`](#envrc) using the
[`direnv`](https://direnv.net/) shell extension, but is **not** tracked by Git.
{% endif %}
### `.secrets.baseline`

Optional baseline file for the [`detect-secrets`](https://github.com/Yelp/detect-secrets) package; this package detects
secrets, and, in conjunction with `pre-commit`, prevents them from being committed to the repository. The baseline file
flags secret-like data that the user deliberately wishes to commit the to repository.

### `Makefile`

The `Makefile` contains a set of commands for the `make` utility. Run the `help` command for further information at the
top-level of the Git repository.

```
make help
```

### `README.md`

An overview of the Git repository, including all necessary instructions to execute the code.

### `requirements.txt`

A list of Python package requirements for this Git repository, which can be installed using the `pip install` command.

```
pip install --requirement requirements.txt
```
