# `{{ cookiecutter.repo_name }}`

{{ cookiecutter.overview }}

> ℹ️ Where this documentation refers to the **root folder** we mean where this README.md is located.

- [Getting started](#getting-started)
  - [Requirements](#requirements)
- [Required secrets and credentials](#required-secrets-and-credentials)
- [Licence](#licence)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Getting started

To start contributing to `{{ cookiecutter.repo_name }}`, run the following commands in your shell:

``` shell script
make requirements
```

### Requirements

> ⚠️ For Windows support, see this [guidance][docs-windows-support].

- A `.secrets` file with the [required secrets and credentials](#required-secrets-and-credentials)
- [Load environment variables][docs-loading-environment-variables] from `.envrc`

To be added.

## Required secrets and credentials

To run this project, you need a `.secrets` file with secrets/credentials as environmental variables; see the
[documentation][docs-loading-environment-variables-secrets] for further guidance. The secrets/credentials should have
the following environment variable name(s):

| Secret/credential | Environment variable name | Description                                |
|-------------------|---------------------------|--------------------------------------------|
| Secret 1          | `SECRET_VARIABLE_1`       | Plain English description of Secret 1.     |
| Credential 1      | `CREDENTIAL_VARIABLE_1`   | Plain English description of Credential 1. |

Once you've added these environment variables to `.secrets` you will need to
[load them via `.envrc`][docs-loading-environment-variables].

## Licence

Unless stated otherwise, the codebase is released under the MIT License. This covers both the codebase and any sample
code in the documentation. The documentation is © Crown copyright and available under the terms of the Open Government
3.0 licence.

## Contributing

If you want to help us build, and improve `{{ cookiecutter.repo_name }}`, view our
[contributing guidelines][contributing].

## Acknowledgements

This project structure is based on the [`govcookiecutter`][govcookiecutter] template project.

[contributing]: ./CONTRIBUTING.md
[govcookiecutter]: https://github.com/ukgovdatascience/govcookiecutter
[docs-loading-environment-variables]: ./docs/user_guide/loading_environment_variables.md
[docs-loading-environment-variables-secrets]: ./docs/user_guide/loading_environment_variables.md#storing-secrets-and-credentials
[docs-windows-support]: ./docs/user_guide/windows_support.md
[pre-commit]: https://pre-commit.com/
