# `docs` folder

Guidance on how to create Sphinx documentation is supplied below. For folder usage, please refer to the documentation
[here](structure/README.md#docs-folder).

## Creating Sphinx documentation

This repository is set up to produce documentation using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) in
either [ReStructuredText](https://www.sphinx-doc.org/en/master/usage/quickstart.html#adding-content) or
[Markdown](#markdown-content).

It can also automatically generate documentation directly from Python docstrings; Python docstrings can be in the
[ReStructuredText](https://www.python.org/dev/peps/pep-0287/),
[NumPy](https://numpydoc.readthedocs.io/en/latest/format.html), or
[Google](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) formats, as supported by the
Sphinx [`napoleon`](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) extension.

### Markdown content

Sphinx uses [`recommonmark`](https://recommonmark.readthedocs.io/en/latest/index.html) to parse Markdown content. This
is based on the [Commonmark](https://commonmark.org/) standard of Markdown, so all content should be written to this
standard.

Markdown tables should be parsed correctly due to the Sphinx
[`sphinx_markdown_tables`](https://github.com/ryanfox/sphinx-markdown-tables) extension.

You can [embed](#embedding-restructuredtext-elements) ReStructuredText elements if required, and also
[reference](#referencing-headings-in-other-documentation-files) other page headings within the `docs` folder.

#### Embedding ReStructuredText elements

> This repository is not set up to include Markdown files outside of the `docs` folder.

To embed ReStructuredText elements in your Markdown documents, use an `eval_rst` codeblock - examples are available in
the `recommonmark` API
[documentation](https://recommonmark.readthedocs.io/en/latest/auto_structify.html#embed-restructuredtext).

#### Referencing headings in other documentation files

To reference headings in other files within the `docs` folder, use the Sphinx `autosectionlabel` extension, as
described in the `recommonmark`
[documentation](https://recommonmark.readthedocs.io/en/latest/index.html#linking-to-headings-in-other-files).

### Automatically documenting Python docstrings

To automatically document Python docstrings from the [`src` package](structure/README.md#src-package), leverage
the Sphinx [`autodoc`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) and
[`autosummary`](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html) extensions.

These extensions provide a summary of the function's docstring in the calling file, and also link to automatically
generated ReStructuredText files of the entire docstring. The
[pandas API reference](https://pandas.pydata.org/pandas-docs/stable/reference/index.html) is an example implementation
of these extensions.

> If you are generating content in Markdown, you need to enter the code below in ``eval_rst`` code blocks. See
> the 'Embedding ReStructuredText elements' section for further details.

First, add a `currentmodule` Sphinx directive pointing to `src` near the top of the file, say after the first heading.

```
.. currentmodule:: src
```

Then add the `autosummary` directive, with a `toctree` element pointing at `api/`; this is a `docs` sub-folder that is
created to store the automatically generated ReStructuredText docstrings. Function names from `src` can then be added
inline.

```
.. autosummary::
    :toctree: api/

    <<<FUNCTION 1>>>
    <<<FUNCTION 2>>>

```

For example, if `src/__init__.py` has functions called `hello` and `world` imported in it, the ReStructuredText
documentation might look like:

```
=======
Heading
=======

This is the reference documentation for the ``src`` package.

.. currentmodule:: src

---------------
``src`` package
---------------

.. autosummary::
    :toctree: api/

    hello
    world

```

A Markdown version would look like this:

````
# Heading

This is the reference documentation for the ``src`` package.

```eval_rst
.. currentmodule:: src

```

## ``src`` package

```eval_rst
.. autosummary::
    :toctree: api/

    hello
    world

```

````
