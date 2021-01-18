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
- [Documentation](#documentation)
- [HM Government department frameworks](#hm-government-department-frameworks)

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

The pre-commit hooks are a security feature to ensure no secrets<sup>[1](#footnote-1)</sup>, large data files, and
Jupyter notebook outputs are accidentally committed into the repository. For more information about the pre-commit
hooks used in this repository, see the [documentation][docs-pre-commit-hooks].

## Code conventions

We mainly follow [The GDS Way][gds-way] in our code conventions.

### Git and GitHub

We use Git to version control the source code; please read [The GDS Way][gds-way-git] for further details, including
information about writing good commit messages, using `git rebase` for local branches, and `git merge --no-ff` for
merges, as well as the entry on `git push --force-with-lease` instead of `git push -f`.

If you want to modify the `.gitignore` files, see the template [documentation][docs-updating-gitignore] for further
details.

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

We also try to wrap Markdown to a line length of 120 characters, but this is not strictly enforced in all cases, for
example with long hyperlinks.

## Testing

Tests are written using the [pytest][pytest] framework, with its configuration in the `pytest.ini` file. Note, only
tests in the `tests`, and `{{ cookiecutter.repo_name }}/tests` folders are executed. To run the tests, execute the
following command in your terminal:

```shell
pytest
```

### Code coverage

Code coverage of Python scripts is measured using the [`coverage`][coverage] Python package; its configuration can be
found in `.coveragerc`. Note coverage only extends to Python scripts in the `hooks`, and
`{{ cookiecutter.repo_name }}/src` folders.

To run code coverage, and view it as an HTML report, execute the following commands in your terminal:

```shell
coverage run -m pytest
coverage html
```

The HTMl report can be accessed at `htmlcov/index.html`.

## Documentation

We write our documentation in [MyST Markdown][myst] for use in Sphinx. This is mainly stored in the `docs` folder,
unless it's more appropriate to store it elsewhere, like this file.

Further information on how to write Sphinx documentation, and how to build it into a searchable website can be found
[here][docs-write-sphinx-documentation].

## HM Government department frameworks

HM Government frameworks are stored in the `.govcookiecutter/department_frameworks` folder. If you would like to add
your own department's framework, follow the [instructions][docs-govcookiecutter-frameworks] in the `README.md` file in
that folder.

---

<a name="footnote-1">[1]</a>: Only secrets of specific patterns are detected by the pre-commit hooks. See
[here][docs-pre-commit-hooks-secrets-definition] for further details.

[code-of-conduct]: ./CODE_OF_CONDUCT.md
[coverage]: https://coverage.readthedocs.io/
[docs-govcookiecutter-frameworks]: ./%7B%7B%20cookiecutter.repo_name%20%7D%7D/.govcookiecutter/department_frameworks/README.md
[docs-pre-commit-hooks]: ./%7B%7B%20cookiecutter.repo_name%20%7D%7D/docs/contributor_guide/pre_commit_hooks.md
[docs-pre-commit-hooks-secrets-definition]: ./%7B%7B%20cookiecutter.repo_name%20%7D%7D/docs/contributor_guide/pre_commit_hooks.md#definition-of-a-secret-according-to-detect-secrets
[docs-updating-gitignore]: ./%7B%7B%20cookiecutter.repo_name%20%7D%7D/docs/contributor_guide/updating_gitignore.md
[docs-write-sphinx-documentation]: ./%7B%7B%20cookiecutter.repo_name%20%7D%7D/docs/contributor_guide/writing_sphinx_documentation.md
[email]: mailto:gdsdatascience@digital.cabinet-office.gov.uk
[gds-way]: https://gds-way.cloudapps.digital/
[gds-way-git]: https://gds-way.cloudapps.digital/standards/source-code.html
[gds-way-python]: https://gds-way.cloudapps.digital/manuals/programming-languages/python/python.html#python-style-guide
[govcookiecutter]: https://github.com/ukgovdatascience/govcookiecutter
[govcookiecutter-frameworks]: ./%7B%7B%20cookiecutter.repo_name%20%7D%7D/.govcookiecutter/department_frameworks
[myst]: https://myst-parser.readthedocs.io/
[pre-commit]: https://pre-commit.com/
[pytest]: https://docs.pytest.org/
[readme-requirements]: ./README.md#requirements-to-create-a-cookiecutter-template
