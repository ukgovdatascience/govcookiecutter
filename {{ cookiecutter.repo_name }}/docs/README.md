# `docs` folder

All documentation for the project should be included in this folder in either reStructuredText or Markdown files, with
acceptable formatting for Sphinx.

To build the documentation, run the `docs` command from the [`Makefile`][docs-makefile] using the `make` utility at the
top-level of this Git repository.

```shell
make docs
```

Guidance on how to write Sphinx documentation is supplied in the [contributor guide][writing-sphinx-documentation].

## Analytical quality assurance (AQA)

All analytical quality assurance (AQA) documents can be found in the `docs/aqa` folder. These files document how this
project meets public sector guidance on producing quality analysis, as described in the [Aqua book][aqua-book].

[aqua-book]: https://www.gov.uk/government/publications/the-aqua-book-guidance-on-producing-quality-analysis-for-government
[docs-makefile]: ../docs/structure/README.md#makefile
[writing-sphinx-documentation]: ../docs/contributor_guide/writing_sphinx_documentation.md
