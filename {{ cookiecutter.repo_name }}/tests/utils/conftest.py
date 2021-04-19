from pathlib import Path
from src.utils.dotenvrc_to_dotenv import _get_source_env_file_path, _read_and_clean_file
from typing import Dict, List
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def create_dummy_text_file(tmp_path: Path, test_input_filename: str, test_input_text: str) -> Path:
    """Create a dummy file with text in it."""
    test_input_filepath = tmp_path.joinpath(test_input_filename)
    with open(test_input_filepath, "w") as f:
        f.write(test_input_text)
    return test_input_filepath


@pytest.fixture
def create_dummy_text_files(tmp_path: Path, test_input_filenames: List[str], test_input_texts: List[str]) -> List[Path]:
    """Create dummy files with text in them."""
    test_input_filepaths = []
    for test_input_filename, test_input_text in zip(test_input_filenames, test_input_texts):
        test_input_filepath = tmp_path.joinpath(test_input_filename)
        with open(test_input_filepath, "w") as f:
            f.write(test_input_text)
        test_input_filepaths.append(test_input_filepath)
    return test_input_filepaths


@pytest.fixture
def patch__read_and_clean_file(mocker) -> MagicMock:
    """Patch the ``_read_and_clean_file`` function."""
    return mocker.patch("src.utils.dotenvrc_to_dotenv._read_and_clean_file", side_effect=_read_and_clean_file)


@pytest.fixture
def patch__get_source_env_file_path(mocker) -> MagicMock:
    """Patch the ``_get_source_env_file_path`` function."""
    return mocker.patch("src.utils.dotenvrc_to_dotenv._get_source_env_file_path", side_effect=_get_source_env_file_path)


@pytest.fixture
def patch__replace_text(mocker) -> MagicMock:
    """Patch the ``_replace_text`` function."""
    return mocker.patch("src.utils.dotenvrc_to_dotenv._replace_text")


@pytest.fixture
def patch__extract_environment_variables_from_export_attributes(mocker) -> MagicMock:
    """Patch the ``_extract_environment_variables_from_export_attributes`` function."""
    return mocker.patch("src.utils.dotenvrc_to_dotenv._extract_environment_variables_from_export_attributes")


@pytest.fixture
def patch__identical_to_existing_env_file(mocker) -> MagicMock:
    """Patch the ``_identical_to_existing_env_file`` function."""
    return mocker.patch("src.utils.dotenvrc_to_dotenv._identical_to_existing_env_file")


@pytest.fixture
def patch__write_file(mocker) -> MagicMock:
    """Patch the ``_write_file`` function."""
    return mocker.patch("src.utils.dotenvrc_to_dotenv._write_file")


@pytest.fixture
def patch_load_dotenv(mocker) -> MagicMock:
    """Patch the ``python-dotenv.load_dotenv`` function."""
    return mocker.patch("src.utils.dotenvrc_to_dotenv.load_dotenv")


@pytest.fixture
def load_dotenvrc_patches(patch__read_and_clean_file: MagicMock, patch__get_source_env_file_path: MagicMock,
                          patch__replace_text: MagicMock,
                          patch__extract_environment_variables_from_export_attributes: MagicMock,
                          patch__identical_to_existing_env_file: MagicMock, patch__write_file: MagicMock,
                          patch_load_dotenv: MagicMock) -> Dict[str, MagicMock]:
    """Compile the patches for the ``load_dotenvrc`` function."""
    return {"_read_and_clean_file": patch__read_and_clean_file,
            "_get_source_env_file_path": patch__get_source_env_file_path, "_replace_text": patch__replace_text,
            "_extract_environment_variables_from_export_attributes":
                patch__extract_environment_variables_from_export_attributes,
            "_identical_to_existing_env_file": patch__identical_to_existing_env_file, "_write_file": patch__write_file,
            "load_dotenv": patch_load_dotenv}
