# `department_frameworks` folder

This folder contains all HM Government department-specific frameworks. Each sub-folder is named for a department, and
the name must be listed in the `departmental_framework` variable in the root-level `cookiecutter.json` file to be used;
see the `GDS` folder for an example framework structure.

```{contents}
:local:
:depth: 2
```

## Analytical quality assurance (AQA) framework

Within each department folder, there must be a `aqa` folder that contains templates for the:

- Analytical quality assurance (AQA) plan; and
- Assumptions and caveats log.

It must also include a `README.md` to link the AQA templates together using in [MyST syntax][myst-parser].

## Pull or merge request template

A `request_template.md` file must be included in each department folder. This will be used to create a pull (GitHub) or
merge (GitLab) request template in the project structure created by `govcookiecutter`.

You should include hints, and nudges to make sure contributors to your department's projects follow its AQA framework.

[aqua-book]: https://www.gov.uk/government/publications/the-aqua-book-guidance-on-producing-quality-analysis-for-government
[aqua-book-resources]: https://www.gov.uk/government/collections/aqua-book-resources
[myst-parser]: https://myst-parser.readthedocs.io/
