from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, List, Optional, Union
import os
import re

# Get the root folder called {{ cookiecutter.repo_name }}  # noqa
DIR_REPOSITORY = [p for p in Path(__file__).parents if p.name == "{{ cookiecutter.repo_name }}"][0]  # noqa

# Define a dictionary of text in the `.envrc` file that need to be replaced; dictionary keys are the text in the
# `.envrc` file, whilst dictionary values are their replacements. `PYTHONPATH` may be empty; if not we want to append
# to the existing variable not replace it - the separator on POSIX machines is ":", but ";" on Windows machines
REPLACEMENTS = {
    "$(pwd)": DIR_REPOSITORY.as_posix(),
    "$PYTHONPATH:": f"{os.getenv('PYTHONPATH')}{':' if os.name == 'posix' else ';'}" if os.getenv("PYTHONPATH") else "",
}


def _read_and_clean_file(file: Union[str, Path]) -> List[str]:
    """Read in a file, and clean out blank lines and comment lines, i.e. lines starting with #.

    Args:
        file: The file path to a file to be read in and clean.

    Returns:
        Parsed contents of the ``file`` with no blank lines or comment lines.

    """
    with open(file) as file_envrc:
        return [L for L in file_envrc.read().splitlines() if not L.startswith("#") and L]


def _get_source_env_file_path(text: str) -> Optional[str]:
    """Extract file path argument for direnv_ ``source_env`` or ``source_env_if_exists`` commands in a piece of text.

    Args:
        text: A piece of text that may or may not contain direnv_ ``source_env`` or ``source_env_if_exists`` commands,
            followed by a file path.

    Returns:
        None if no ``source_env`` or ``source_env_if_exists`` commands were found in ``text``, otherwise the file path
        argument from this command.

    .. _direnv: https://direnv.net/man/direnv-stdlib.1.html#codesourceenv-ltfileordirpathgtcode

    """

    # Full match using regular expressions for `source_env` or ``source_env_if_exists`` commands to extract out the
    # file path argument
    pattern = r"^source_env\w* [\"'](?P<file>.+)[\"']$"
    pattern_match = re.fullmatch(pattern, text)

    # If there is match, extract out the file path argument, otherwise return None
    return pattern_match.group("file") if pattern_match else None


def _replace_text(text: str, replacements: Dict[str, str]) -> str:
    """Make multiple replacements in a given piece of text.

    Args:
        text: A text for replacement containing strings to be replaced.
        replacements: A dictionary of string-replacement pairs to be replaced in ``text``.

    Returns:
        ``text`` with all replacements made.

    """
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def _extract_environment_variables_from_export_attributes(text: str) -> Optional[str]:
    """Extract environment variables from ``export`` attributes using regular expressions.

    Args:
        text: A piece of text that may or may not contain ``export`` attributes of environment variables of the form
            ``export NAME=VALUE``, where ``VALUE`` can be a quoted or unquoted.

    Returns:
        The environment variable as ``NAME=VALUE`` with ``VALUE`` unquoted if any, otherwise None is returned.

    """

    # Full match using regular expressions for `export` attributes to extract out name and value pairs. Run two
    # matches: one for when the value is in quotes (" or '), and one for when the value is unquoted
    pattern = r"^export (?P<name_quoted>\w+)=[\"'](?P<value_quoted>.+)[\"']|" \
              r"^export (?P<name_unquoted>\w+)=(?P<value_unquoted>.+)$"
    pattern_match = re.fullmatch(pattern, text)

    # If there is a match, determine if the value is quoted or not, and return the correct name-value pair as a
    # equals-delimited string. Otherwise, if no match, return None
    if pattern_match:
        if pattern_match.group("value_quoted"):
            return f"{pattern_match.group('name_quoted')}={pattern_match.group('value_quoted')}"
        else:
            return f"{pattern_match.group('name_unquoted')}={pattern_match.group('value_unquoted')}"
    else:
        return None


def _identical_to_existing_env_file(env: Union[str, Path], env_variables: List[str]):
    """Check if the pre-calculated ``.env`` variables match an existing ``.env`` file.

    Args:
        env: A file path to the existing ``.env`` file.
        env_variables: Pre-calculated ``.env`` variables as a list of strings to compare with ``env``.

    Returns:
        True/False depending if ``env_variables`` match the existing ``env`` file. If ``env`` does not exist, always
        return False.

    """
    try:
        with open(env) as f:
            return set(f.read().splitlines()) == set(env_variables)
    except FileNotFoundError:
        return False


def _write_file(strings: List[str], filename: Union[str, Path]) -> None:
    """Write out a list of strings to a file.

    Args:
        strings: A list of strings containing variables to be written out to a ``filename`` file.
        filename: A file path where ``strings`` should be written out to.

    Returns:
        A file containing ``strings`` delimited by new lines at the file path specified by ``filename``.

    """
    with open(filename, "w") as out:
        out.write("\n".join(strings))


def load_dotenvrc(envrc: Union[str, Path, None] = None, replacements: Optional[Dict[str, str]] = None,
                  env: Union[str, Path, None] = None, load_env: bool = True,
                  override_existing_env: bool = True) -> None:
    """Convert a ``.envrc`` file to a "name=variable" pairs.

    If ``load_env`` is True (default), a comparison will be made to an existing ``.env`` file (if any) - if they are
    different, this function will overwrite the ``.env`` file. Then the ``.env`` file is loaded in. If
    ``override_existing_env`` is also set to True (default), any existing environment variables with the same name will
    be overwritten.

    Also loads any file path arguments to `direnv`_ ``source_env`` and ``source_env_if_exists`` commands.

    Args:
        envrc: Default: None. A file path to a ``.envrc`` file. If None, will assume the ``.envrc`` file is at the
            repository root folder.
        replacements: Default: None. A dictionary of string-replacement values to replace values in ``envrc``. If None,
            will default to the ``REPLACEMENTS`` variable defined in ``src/utils/load_dotenvrc.py``.
        env: Default: None. A file path to a ``.env`` file. If None, will read/write to the repository root folder.
        load_env: Default: True. If True, will automatically load the ``env``.
        override_existing_env: Default: True. If True, will override any existing environment variables when ``env`` is
            loaded. Only valid if ``load_env`` is also True.

    Returns:
        Creates a new ``.env`` file if different to an existing ``.env`` file or if no ``.env`` file already exists,
        based on the ``.envrc`` file. If ``load_env`` is True, the ``.env`` file is loaded as well. If ``load_env`` and
        ``override_existing_env`` are True, the ``.env`` file is loaded, and its environment variables will override
        any existing environment variables - see the python-dotenv package `documentation`_ for the ``override``
        argument for further details.

    .. _direnv: https://direnv.net/man/direnv-stdlib.1.html#codesourceenv-ltfileordirpathgtcode
    .. _documentation: https://saurabh-kumar.com/python-dotenv/#variable-expansion

    """

    # Define default file paths to a `.envrc` and `.env` file if not already specified
    envrc = envrc if envrc else DIR_REPOSITORY.joinpath(".envrc")
    env = env if env else DIR_REPOSITORY.joinpath(".env")

    # Define default replacements if not already assigned
    replacements = replacements if replacements else REPLACEMENTS

    # Assert `replacements` values are not in keys, as this may result in unexpected behaviour
    assert not (set(replacements.keys()) & set(replacements.values()))

    # Parse the `.envrc` file
    parsed_envrc = _read_and_clean_file(envrc)

    # Get all file paths listed for `source_env` or `source_env_if_exists` commands in the `.envrc` file
    parsed_source_env_nested_files = [
        _read_and_clean_file(Path(envrc).parent.joinpath(f)) for f in map(_get_source_env_file_path, parsed_envrc) if f
    ]

    # Extract all export attribute name-value pairs as "name=value" in `.envrc` and any files found in
    # `parsed_source_env_nested_files`, dropping any None values
    env_variables = list(map(
        lambda l: _extract_environment_variables_from_export_attributes(_replace_text(l, replacements)),
        parsed_envrc + [L for n in parsed_source_env_nested_files for L in n]
    ))
    env_variables = [e for e in env_variables if e]

    # If there is an existing `.env` file, check if `env_variables` matches its contents. If not, write a new `.env`
    # file
    if not _identical_to_existing_env_file(env, env_variables):
        _write_file(env_variables, env)

    # If `load_env` is True, load the `.env` file. Override any existing environment variables if
    # `override_existing_env` is True
    if load_env:
        _ = load_dotenv(env, override=override_existing_env)
