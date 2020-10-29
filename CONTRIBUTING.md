# Contributing

We love contributions! We've compiled this documentation to help you understand our contributing guidelines. If you
still have questions, please [contact us][email] and we'd be happy to help!

- [Code of Conduct](#code-of-conduct)
- [Getting started](#getting-started)
- [Code conventions](#code-conventions)
  - [Git and GitHub](#git-and-github)
  - [Python](#python)
  - [Markdown](#markdown)
- [Testing](#testing)

## Code of Conduct

Please read [`CODE_OF_CONDUCT.md`][code-of-conduct] before contributing.

## Getting started

To start contributing, first ensure your system meets the [requirements][readme-requirements]. Next, install the
required Python packages, and [pre-commit hooks][pre-commit] using:

```shell
make requirements
```

It is better to use the above make command, rather than `pip install -r requirements.txt` and `pre-commit install`, as
the command will ensure your pre-commit hooks are up-to-date with any changes made.

The pre-commit hooks are a security feature to ensure no secrets, large data files, and Jupyter notebooks are
accidentally committed into the repository.

## Code conventions

We mainly follow [The GDS Way][gds-way] in our code conventions.

### Git and GitHub

We use Git to version control the source code; please read [The GDS Way][gds-way-git] for further details, including
information about writing good commit messages, using `git rebase` for local branches, and `git merge --no-ff` for
merges, as well as the entry on `git push --force-with-lease` instead of `git push -f`.

Our source code is stored on GitHub at [https://github.com/ukgovdatascience/govcookiecutter][govcookiecutter]. Pull
requests into `master` require at least one approved review.

### Python

For Python code, we follow [The GDS Way Python style guide][gds-way-python] with a line length of 120; the flake8
pre-commit hook should help with this!

### Markdown

Local links can be written as normal, but external links should be referenced at the bottom of the Markdown file for
clarity. For example:

```md
Use a local link to reference the [`README.md`](./README.md) file, but an external link for [GOV.UK][gov-uk].

[gov-uk]: https://www.gov.uk/
```

We also try and wrap Markdown to a line length of 120 characters, but this is not strictly enforced in all cases, for
example with long hyperlinks.

## Testing

Tests are written using the [pytest][pytest] framework, with its configuration in the [`pytest.ini`][pytest-ini].
Note, only tests in the [`tests`][tests] and [`{{ cookiecutter.repo_name }}/tests`][tests-template] folder are
executed. To run the tests, execute the following command in your terminal:

```shell
pytest
```

### Code coverage

Code coverage of Python scripts is measured using the [`coverage`][coverage] Python package; its configuration can be
found in [`.coveragerc`][coveragerc]. Note coverage only extends to Python scripts in the [`hooks`][hooks], and
[`{{ cookiecutter.repo_name }}/src`][src-template] folders.

To run code coverage, and view it as a HTML report, execute the following commands in your terminal:

```shell
coverage run -m pytest
coverage html
```

The HTMl report can be accessed at `htmlcov/index.html`.

[code-of-conduct]: ./CODE_OF_CONDUCT.md
[coverage]: https://coverage.readthedocs.io/
[coveragerc]: ./.coveragerc
[email]: mailto:gdsdatascience@digital.cabinet-office.gov.uk
[gds-way]: https://gds-way.cloudapps.digital/
[gds-way-git]: https://gds-way.cloudapps.digital/standards/source-code.html
[gds-way-python]: https://gds-way.cloudapps.digital/manuals/programming-languages/python/python.html#python-style-guide
[govcookiecutter]: https://github.com/ukgovdatascience/govcookiecutter
[hooks]: ./hooks
[pre-commit]: https://pre-commit.com/
[pytest]: https://docs.pytest.org/
[pytest-ini]: ./pytest.ini
[readme-requirements]: ./README.md#requirements
[src-template]: ./%7B%7B%20cookiecutter.repo_name%20%7D%7D/src
[tests]: ./tests
[tests-template]: ./%7B%7B%20cookiecutter.repo_name%20%7D%7D/tests