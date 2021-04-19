from collections import OrderedDict
from dotenv import dotenv_values
from pathlib import Path
from src.utils.dotenvrc_to_dotenv import (
    DIR_REPOSITORY,
    REPLACEMENTS,
    _extract_environment_variables_from_export_attributes,
    _get_source_env_file_path,
    _identical_to_existing_env_file,
    _read_and_clean_file,
    _replace_text,
    _write_file,
    load_dotenvrc
)
from typing import Any, Dict, List, Optional
from unittest.mock import DEFAULT, MagicMock, call
import pytest

# Define test cases for the `test__read_and_clean_file` test
args__read_and_clean_file = [
    ("hello.world", "Some text\nSome more text."),
    (".envrc", "export DIR_DATA=$(pwd)/data\nexport DIR_DATA_RAW=$(pwd)/data/raw"),
    (".env", "DIR_DATA=$(pwd)/data\nDIR_DATA_RAW=$(pwd)/data/raw"),
]


@pytest.mark.parametrize("test_input_filename, test_input_text", args__read_and_clean_file)
def test__read_and_clean_file(create_dummy_text_file: str, test_input_text: str) -> None:
    """Test the ``_read_and_clean_file`` function returns as expected."""
    assert "\n".join(_read_and_clean_file(create_dummy_text_file)) == test_input_text


# Define test cases for the `test__replace_text` test
args__replace_text = [
    ("Here is some text", {"some": "other"}, "Here is other text"),
    ("Some text, some more text", {"some": "other", "more": "additional"}, "Some text, other additional text"),
    ("Swap this and that with that and this", {"this": "that", "that": "this"},
     "Swap this and this with this and this"),
]


@pytest.mark.parametrize("test_input_text, test_input_replacements, test_expected", args__replace_text)
def test__replace_text(test_input_text: str, test_input_replacements: Dict[str, str], test_expected: str) -> None:
    """Test the ``_replace_text`` function returns as expected."""
    assert _replace_text(test_input_text, test_input_replacements) == test_expected


# Define test cases for the `test__get_source_env_file_path` test
args__get_source_env_file_path = [
    ("Some text", None),
    ("source_env", None),
    ("source_env_if_exists ", None),
    ("source_env test.file", None),
    ("source_env_if_exists .secrets", None),
    ("source_env 'test.file'", "test.file"),
    ("source_env_if_exists '.secrets'", ".secrets"),
    ("source_env \"test.file\"", "test.file"),
    ("source_env_if_exists \".secrets\"", ".secrets"),
]


@pytest.mark.parametrize("test_input, test_expected", args__get_source_env_file_path)
def test__get_source_env_file_path(test_input: str, test_expected: Optional[str]) -> None:
    """Test the ``_get_source_env_file_path`` function returns as expected."""
    if test_expected:
        assert _get_source_env_file_path(test_input) == test_expected
    else:
        assert _get_source_env_file_path(test_input) is None


# Define test cases for the `test__extract_environment_variables_from_export_attributes` test
args__extract_environment_variables_from_export_attributes = [
    ("hello world", None),
    ("export", None),
    ("export ", None),
    ("export some_text", None),
    ("export some_text and other text", None),
    ("export name=value", "name=value"),
    ("export name='value'", "name=value"),
    ("export name=\"value\"", "name=value"),
]


@pytest.mark.parametrize("test_input, test_expected", args__extract_environment_variables_from_export_attributes)
def test__extract_environment_variables_from_export_attributes(test_input, test_expected) -> None:
    """Test the ``_extract_environment_variables_from_export_attributes`` function returns as expected."""
    if test_expected:
        assert _extract_environment_variables_from_export_attributes(test_input) == test_expected
    else:
        assert _extract_environment_variables_from_export_attributes(test_input) is None


# Define test cases for the `TestIdenticalToExistingEnvFile` test class
args__identical_to_existing_env_file = [
    ("hello.world", "a=b\nc=d\n", ["a=b", "c=d"], True),
    (".env", "a=b\nc=d", ["c=d", "a=b"], True),
    (".env", "a=b\nc=d\n", ["a=b", "c=e"], False),
]


class TestIdenticalToExistingEnvFile:

    @pytest.mark.parametrize("test_input_env_variables", [a[2] for a in args__identical_to_existing_env_file])
    def test_returns_correctly_for_no_env_file(self, test_input_env_variables: List[str]) -> None:
        """Test the ``_identical_to_existing_env_file`` function returns as expected if the file does not exist."""
        assert not _identical_to_existing_env_file("non_existent.file", test_input_env_variables)

    @pytest.mark.parametrize("test_input_filename, test_input_text, test_input_env_variables, test_expected",
                             args__identical_to_existing_env_file)
    def test_returns_correctly_for_env_file(self, create_dummy_text_file: str, test_input_env_variables: List[str],
                                            test_expected: bool) -> None:
        """Test the ``_identical_to_existing_env_file`` function returns as expected if the file exists."""
        assert _identical_to_existing_env_file(create_dummy_text_file, test_input_env_variables) == test_expected


# Define test cases for the `test__write_file` test
args__write_file = [
    (["a", "b", "c"], ".env", "a\nb\nc"),
    (["hello world", "foo bar"], ".test", "hello world\nfoo bar")
]


@pytest.mark.parametrize("test_input_strings, test_input_filename, test_expected", args__write_file)
def test__write_file(tmpdir, test_input_strings: List[str], test_input_filename: str, test_expected: str) -> None:
    """Test the ``_write_file`` function returns as expected."""

    # Create a temporary file, and write out the data, then parse it and assert it is as expected
    test_file_path = tmpdir.join(test_input_filename)
    _write_file(test_input_strings, test_file_path)
    with open(test_file_path) as f:
        assert f.read() == test_expected


# Define test cases for the `TestIntegrationLoadDotenvrc` test class
args_integration__read_and_clean_file = [
    (".file1", "export A=1\nexport B=2\nexport C=3", [".file1"]),
    (".file2", "export A=1\nsource_env \"b\"\nexport C=3", [".file2", "b"]),
    (".file2", "export A=1\nsource_env 'b'\nexport C=3", [".file2", "b"]),
    (".file3", "export A=1\nsource_env \"b\"\nexport C=3\nsource_env_if_exists 'd'", [".file3", "b", "d"]),
    (".file3", "export A=1\nsource_env 'b'\nexport C=3\nsource_env_if_exists \"d\"", [".file3", "b", "d"]),
]
args_integration__get_source_env_file_path = [
    (".file1", "export A=1\nexport B=2\nexport C=3", ["export A=1", "export B=2", "export C=3"]),
    (".file2", "export A=1\nsource_env \"b\"\nexport C=3", ["export A=1", "source_env \"b\"", "export C=3"]),
    (".file2", "export A=1\nsource_env 'b'\nexport C=3", ["export A=1", "source_env 'b'", "export C=3"]),
    (".file3", "export A=1\nsource_env \"b\"\nexport C=3\nsource_env_if_exists 'd'",
     ["export A=1", "source_env \"b\"", "export C=3", "source_env_if_exists 'd'"]),
    (".file3", "export A=1\nsource_env 'b'\nexport C=3\nsource_env_if_exists \"d\"",
     ["export A=1", "source_env 'b'", "export C=3", "source_env_if_exists \"d\""]),
]
args_integration__replace_text = [
    ([".file1"], ["export A=1\nexport B=2"], ["export A=1", "export B=2"]),
    ([".file1", ".file2"], ["export A=1\nexport B=2\nsource_env \".file2\"", "export C=3"],
     ["export A=1", "export B=2", "source_env \".file2\"", "export C=3"]),
    ([".file1", ".file2", ".file3"],
     ["export A=1\nsource_env \".file2\"\nexport B=2\nsource_env '.file3'", "export C=3", "export D=4"],
     ["export A=1", "source_env \".file2\"", "export B=2", "source_env '.file3'", "export C=3", "export D=4"]),
]
args_integration__replace_text__replacements = [None, {"a": 1, "b": 2}, {"c": 3, "d": 4}]
args_integration__extract_environment_variables_from_export_attributes = [
    ([".file1"], ["export A=1\nexport B=2"], 2),
    ([".file1", ".file2"], ["export A=1\nexport B=2\nsource_env \".file2\"", "export C=3"], 4),
    ([".file1", ".file2", ".file3"],
     ["export A=1\nsource_env \".file2\"\nexport B=2\nsource_env '.file3'", "export C=3", "export D=4"], 6),
]
args_integration__identical_to_existing_env_file = \
    args_integration__extract_environment_variables_from_export_attributes
args_integration__identical_to_existing_env_file__env = [None, ".test_env"]
args_integration__write_file = args_integration__extract_environment_variables_from_export_attributes
args_integration__write_file__env = args_integration__identical_to_existing_env_file__env
args_integration_load_dotenv = [
    ([".file1"], ["export A=1\nexport B=2"]),
    ([".file1", ".file2"], ["export A=1\nexport B=2\nsource_env \".file2\"", "export C=3"]),
    ([".file1", ".file2", ".file3"],
     ["export A=1\nsource_env \".file2\"\nexport B=2\nsource_env '.file3'", "export C=3", "export D=4"]),
]
args_integration_load_dotenv__env = args_integration__identical_to_existing_env_file__env
args_integration_load_dotenv_after__write_file = [
    ([".file1", ".file2"], ["export A=1", "A=1"]),
    ([".file1", ".file2"], ["export A=1\nexportB=2", "A=1\nB=2"])
]


class TestIntegrationLoadDotenvrc:

    def test__read_and_clean_file_uses_default_envrc(self, load_dotenvrc_patches: Dict[str, MagicMock]) -> None:
        """Test the ``_read_and_clean_file`` function is called correctly if ``envrc=None``."""

        # Execute the `load_dotenvrc` and assert `_read_and_clean_file` is called with both the `.envrc` and `.secrets`
        # file paths
        load_dotenvrc(envrc=None)
        load_dotenvrc_patches["_read_and_clean_file"].assert_has_calls(
            [call(DIR_REPOSITORY.joinpath(".envrc")), call(DIR_REPOSITORY.joinpath(".secrets"))]
        )

    @pytest.mark.parametrize("test_input_filename, test_input_text, test_expected",
                             args_integration__read_and_clean_file)
    def test__read_and_clean_file_called_correctly(self, load_dotenvrc_patches: Dict[str, MagicMock],
                                                   create_dummy_text_file: str, test_expected: List[str]) -> None:
        """Test the ``_read_and_clean_file`` function is called correctly."""

        # Define the file path to the ".envrc" file, and then any subsequent sourced files, if relevant
        test_input_file = Path(create_dummy_text_file)
        test_expected_files = [call(test_input_file),
                               *[call(test_input_file.parent.joinpath(f)) for f in test_expected[1:]]]

        # Set the side effect of the `_read_and_clean_file` patch. Use `DEFAULT` to restore normal MagicMock side
        # effects after the first call of `_read_and_clean_file` - must be the same as number of times we expect
        # `_read_and_clean_file` to be called (minus the first call), otherwise a `StopIteration` error is returned
        load_dotenvrc_patches["_read_and_clean_file"].side_effect = [_read_and_clean_file(test_input_file),
                                                                     *[DEFAULT] * len(test_expected[1:])]

        # Execute the `load_dotenvrc` function, and assert it is called with the correct arguments in the correct order
        load_dotenvrc(envrc=test_input_file)
        load_dotenvrc_patches["_read_and_clean_file"].assert_has_calls(test_expected_files)

    @pytest.mark.parametrize("test_input_filename, test_input_text, test_expected",
                             args_integration__get_source_env_file_path)
    def test__get_source_env_file_path_called_correctly(self, load_dotenvrc_patches: Dict[str, MagicMock],
                                                        create_dummy_text_file: str, test_expected: List[str]) -> None:
        """Test the ``_get_source_env_file_path`` function is called correctly."""

        # Set the side effect of the `_read_and_clean_file` patch. Use `DEFAULT` to restore normal MagicMock side
        # effects after the first call of `_read_and_clean_file` - must be the same as number of times we expect
        # `_read_and_clean_file` to be called (minus the first call), otherwise a `StopIteration` error is returned
        load_dotenvrc_patches["_read_and_clean_file"].side_effect = [_read_and_clean_file(create_dummy_text_file),
                                                                     *[DEFAULT] * len(test_expected[1:])]

        # Execute the `load_dotenvrc` function, and assert it is called with the correct arguments in the correct order
        load_dotenvrc(envrc=create_dummy_text_file)
        load_dotenvrc_patches["_get_source_env_file_path"].assert_has_calls([call(e) for e in test_expected])

    @pytest.mark.parametrize("test_input_filenames, test_input_texts, test_expected", args_integration__replace_text)
    @pytest.mark.parametrize("test_input_replacements", args_integration__replace_text__replacements)
    def test__replace_text_called_correctly(self, load_dotenvrc_patches: Dict[str, MagicMock],
                                            create_dummy_text_files: List[Path],
                                            test_input_replacements: Optional[Dict[str, Any]],
                                            test_expected: List[str]) -> None:
        """Test the ``_replace_text`` function is called correctly."""

        # Execute the `load_dotenvrc` using the first file in `create_dummy_text_files` as `.envrc`
        load_dotenvrc(envrc=create_dummy_text_files[0], replacements=test_input_replacements)

        # Assert the calls are as expected
        test_input_replacements = test_input_replacements if test_input_replacements else REPLACEMENTS
        test_expected_calls = [call(e, test_input_replacements) for e in test_expected]
        load_dotenvrc_patches["_replace_text"].assert_has_calls(test_expected_calls)

    @pytest.mark.parametrize("test_input_filenames, test_input_texts, test_expected_call_count",
                             args_integration__extract_environment_variables_from_export_attributes)
    def test__extract_environment_variables_from_export_attributes_called_correctly(
            self, load_dotenvrc_patches: Dict[str, MagicMock], create_dummy_text_files: List[Path],
            test_expected_call_count: int
    ) -> None:
        """Test the ``_extract_environment_variables_from_export_attributes`` function is called correctly."""

        # Execute the `load_dotenvrc` using the first file in `create_dummy_text_files` as `.envrc`
        load_dotenvrc(envrc=create_dummy_text_files[0])

        # Assert the calls are as expected
        load_dotenvrc_patches["_extract_environment_variables_from_export_attributes"].assert_has_calls(
            [call(load_dotenvrc_patches["_replace_text"].return_value)] * test_expected_call_count
        )

    @pytest.mark.parametrize("test_input_filenames, test_input_texts, test_expected_call_count",
                             args_integration__identical_to_existing_env_file)
    @pytest.mark.parametrize("test_input_env", args_integration__identical_to_existing_env_file__env)
    def test__identical_to_existing_env_file_called_correctly(self, load_dotenvrc_patches: Dict[str, MagicMock],
                                                              create_dummy_text_files: List[Path],
                                                              test_input_env: Optional[str],
                                                              test_expected_call_count: int) -> None:
        """Test the ``_identical_to_existing_env_file`` function is called correctly."""

        # Execute the `load_dotenvrc` using the first file in `create_dummy_text_files` as `.envrc`
        load_dotenvrc(envrc=create_dummy_text_files[0], env=test_input_env)

        # Assert the calls are as expected
        load_dotenvrc_patches["_identical_to_existing_env_file"].assert_called_once_with(
            test_input_env if test_input_env else DIR_REPOSITORY.joinpath(".env"),
            [load_dotenvrc_patches["_extract_environment_variables_from_export_attributes"].return_value]
            * test_expected_call_count
        )

    def test__write_file_not_called_correctly(self, load_dotenvrc_patches: Dict[str, MagicMock]):

        # Set the return value of the `_identical_to_existing_env_file` patch to be False
        load_dotenvrc_patches["_identical_to_existing_env_file"].return_value = True

        # Execute the `load_dotenvrc`, and assert the `_write_file` is not called
        load_dotenvrc()
        load_dotenvrc_patches["_write_file"].assert_not_called()

    @pytest.mark.parametrize("test_input_filenames, test_input_texts, test_expected_call_count",
                             args_integration__write_file)
    @pytest.mark.parametrize("test_input_env", args_integration__write_file__env)
    def test__write_file_called_correctly(self, load_dotenvrc_patches: Dict[str, MagicMock],
                                          create_dummy_text_files: List[Path], test_input_env: Optional[str],
                                          test_expected_call_count: int) -> None:
        """Test the ``_write_file`` function is called correctly."""

        # Set the return value of the `_identical_to_existing_env_file` patch to be False
        load_dotenvrc_patches["_identical_to_existing_env_file"].return_value = False

        # Execute the `load_dotenvrc` using the first file in `create_dummy_text_files` as `.envrc`
        load_dotenvrc(envrc=create_dummy_text_files[0], env=test_input_env)

        # Assert the calls are as expected
        load_dotenvrc_patches["_write_file"].assert_called_once_with(
            [load_dotenvrc_patches["_extract_environment_variables_from_export_attributes"].return_value]
            * test_expected_call_count,
            test_input_env if test_input_env else DIR_REPOSITORY.joinpath(".env")
        )

    @pytest.mark.parametrize("test_input_filenames, test_input_texts", args_integration_load_dotenv)
    @pytest.mark.parametrize("test_input_env", args_integration_load_dotenv__env)
    @pytest.mark.parametrize("test_input_load_env", [True, False])
    @pytest.mark.parametrize("test_input_override_existing_env", [True, False])
    def test_load_dotenv_called_correctly(self, load_dotenvrc_patches: Dict[str, MagicMock],
                                          create_dummy_text_files: List[Path], test_input_env: Optional[str],
                                          test_input_load_env: bool, test_input_override_existing_env: bool) -> None:
        """Test the ``load_dotenv`` function is called correctly."""

        # Execute the `load_dotenvrc` using the first file in `create_dummy_text_files` as `.envrc`
        load_dotenvrc(envrc=create_dummy_text_files[0], env=test_input_env, load_env=test_input_load_env,
                      override_existing_env=test_input_override_existing_env)

        # Assert the function is called correctly
        if test_input_load_env:
            load_dotenvrc_patches["load_dotenv"].assert_called_once_with(
                test_input_env if test_input_env else DIR_REPOSITORY.joinpath(".env"),
                override=test_input_override_existing_env
            )
        else:
            load_dotenvrc_patches["load_dotenv"].assert_not_called()

    @pytest.mark.parametrize("test_input_filenames, test_input_texts", args_integration_load_dotenv_after__write_file)
    def test_load_dotenv_after__write_file(self, mocker, load_dotenvrc_patches: Dict[str, MagicMock],
                                           create_dummy_text_files: List[Path], test_input_texts: List[str]) -> None:
        """Test the ``load_dotenv`` function is called after the ``__write_file`` function."""

        # Define a Mock object, and attach mocks to it in the order of execution
        manager = mocker.Mock()
        manager.attach_mock(load_dotenvrc_patches["_write_file"], "w")
        manager.attach_mock(load_dotenvrc_patches["load_dotenv"], "l")

        # Set the return value of the `_identical_to_existing_env_file` patch to be False, and set the side effect of
        # the `_write_file` patch
        load_dotenvrc_patches["_identical_to_existing_env_file"].return_value = False

        # Define the input files
        test_input_envrc, test_input_env = create_dummy_text_files

        # Execute the `load_dotenvrc` using the first file in `create_dummy_text_files` as `.envrc`, and the second
        # file as the `.env` file
        load_dotenvrc(envrc=test_input_envrc, env=test_input_env)

        # Define the expected order of calls, and assert that this is as expected
        test_expected_calls = [
            call.w([load_dotenvrc_patches["_extract_environment_variables_from_export_attributes"].return_value]
                   * (test_input_texts[0].count("\n") + 1),
                   test_input_env),
            call.l(test_input_env, override=True)
        ]
        assert manager.mock_calls == test_expected_calls


# Define test cases for the `test_load_dotenvrc_returns_correctly` test
args_load_dotenvrc_returns_correctly = [
    ([".file0", ".file1"],
     ["A=1\nB=2\n", "export A=1\nexport B=2\n"],
     {},
     {"A": "1", "B": "2"}),
    ([".file0", ".file1", ".file2"],
     ["A=1\nB=2\n", "export A=1\nexport B=2\nsource_env '.file2'", "export C=3"],
     {},
     {"A": "1", "B": "2", "C": "3"}),
    ([".file0", ".file1", ".file2"], ["A=1\nB=2\n", "export A=1\nexport B=2\nsource_env \".file2\"", "export C=3"],
     {},
     {"A": "1", "B": "2", "C": "3"}),
    ([".file0", ".file1", ".file2"],
     ["A=1\nB=2\n", "export A=1\nexport B=2\nsource_env_if_exists '.file2'", "export C=3"],
     {},
     {"A": "1", "B": "2", "C": "3"}),
    ([".file0", ".file1", ".file2"],
     ["A=1\nB=2\n", "export A=1\nexport B=2\nsource_env_if_exists \".file2\"", "export C=3"],
     {},
     {"A": "1", "B": "2", "C": "3"}),
    ([".file0", ".file1", ".file2"],
     ["A=1", "export A=$(abc)\nsource_env '.file2'", "export B=$(def)"],
     {"$(abc)": "5", "$(def)": "9"},
     {"A": "5", "B": "9"}),
    ([".file0", ".file1", ".file2", ".file3"],
     ["A=3", "source_env_if_exists \".file3\"\nexport A=$(abc)\nsource_env '.file2'", "export B=$(def)", "export C=10"],
     {"$(abc)": "5", "$(def)": "9"},
     {"A": "5", "C": "10", "B": "9"}),
]


@pytest.mark.parametrize("test_input_filenames, test_input_texts, test_input_replacements, test_expected",
                         args_load_dotenvrc_returns_correctly)
@pytest.mark.parametrize("test_input_override_existing_env", [True, False])
def test_load_dotenvrc_returns_correctly(capfd, patch_load_dotenv: MagicMock, create_dummy_text_files: List[Path],
                                         test_input_replacements: Dict[str, str],
                                         test_input_override_existing_env: bool, test_expected: Dict[str, Any]) -> None:
    """Test that the ``load_dotenvrc`` function returns correctly."""

    # Set the `load_dotenv` patch to print `.env` values
    patch_load_dotenv.side_effect = lambda args, **kwargs: print(dotenv_values(args))

    # Execute the `load_dotenvrc` function, and assert the correct environment variables are printed; assume the first
    # file is the `.env` file, and the second is the `.envrc` file
    load_dotenvrc(create_dummy_text_files[1], test_input_replacements, create_dummy_text_files[0],
                  override_existing_env=test_input_override_existing_env)
    assert capfd.readouterr()[0] == f"{OrderedDict(test_expected)}\n"
