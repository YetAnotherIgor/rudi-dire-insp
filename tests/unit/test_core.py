"""
Unit tests for the rudi_dire_insp.core module.
"""

# Core python imports
import hashlib
import io
import logging

# 3rd party imports
import pytest

# Imports of code-under-test
import rudi_dire_insp.exceptions as my_exceptions
import rudi_dire_insp.core as my_core

# Module variables
_LOGGER = logging.getLogger(__name__)
pytestmark = pytest.mark.unit


def test_w_missing_root_dir(tmp_path):
    """Test error handling when attempting to inspect a non-existent root directory path"""
    _LOGGER.debug("Begin")

    root_dir_path = tmp_path / "i-dont-exist"

    with pytest.raises(my_exceptions.DirInspectionError) as error_1:
        my_core._FileInspector(str(root_dir_path))
    assert "does not exist" in str(error_1)

    dir_inspector = my_core.DirectoryInspector()
    with pytest.raises(my_exceptions.DirInspectionError) as error_2:
        for _ in dir_inspector.inspect(str(root_dir_path)):
            pass
    assert "does not exist" in str(error_2)

    _LOGGER.debug("Finished")


def test_w_non_dir_root_dir(tmp_path):
    """Test error handling when attempting to inspect a root directory path that doesn't point to a directory"""
    _LOGGER.debug("Begin")

    root_dir_path = tmp_path / "i-am-not-a-directory.txt"
    root_dir_path.write_text("Still not a directory!")

    with pytest.raises(my_exceptions.DirInspectionError) as error_1:
        my_core._FileInspector(str(root_dir_path))
    assert "is not a directory" in str(error_1)

    dir_inspector = my_core.DirectoryInspector()
    with pytest.raises(my_exceptions.DirInspectionError) as error_2:
        for _ in dir_inspector.inspect(str(root_dir_path)):
            pass
    assert "is not a directory" in str(error_2)

    _LOGGER.debug("Finished")


def test_w_invalid_sub_dir(tmp_path):
    """Test error handling when attempting to inspect a sub directory which isn't under the root inspection directory"""
    _LOGGER.debug("Begin")

    dir_not_under_root_path = tmp_path / "not-under-stuff"
    dir_not_under_root_path.mkdir()
    root_dir_path = tmp_path / "stuff"
    root_dir_path.mkdir()
    file_path = dir_not_under_root_path / "test.txt"
    file_path.write_text("hello world")

    inspector = my_core._FileInspector(str(root_dir_path))

    with pytest.raises(my_exceptions.FileInspectionError) as error_1:
        inspector.inspect(str(file_path))
    assert "not a child of the root directory path" in str(error_1)
    _LOGGER.debug("Finished")


def test_w_missing_file(tmp_path):
    """Test error handling when attempting to inspect an non-existent file"""
    _LOGGER.debug("Begin")

    root_dir_path = tmp_path / "stuff"
    root_dir_path.mkdir()
    file_path = root_dir_path / "test.txt"

    inspector = my_core._FileInspector(str(root_dir_path))

    with pytest.raises(my_exceptions.FileInspectionError) as error_1:
        inspector.inspect(str(file_path))
    assert "File at path does not exist" in str(error_1)
    _LOGGER.debug("Finished")


def test_w_file_thats_not_a_file(tmp_path):
    """Test error handling when attempting to inspect an file that isn't a file"""
    _LOGGER.debug("Begin")

    root_dir_path = tmp_path / "stuff"
    root_dir_path.mkdir()
    file_path = root_dir_path / "test.txt"
    file_path.mkdir()

    inspector = my_core._FileInspector(str(root_dir_path))

    with pytest.raises(my_exceptions.FileInspectionError) as error_1:
        inspector.inspect(str(file_path))
    assert "Path does not point to a file" in str(error_1)
    _LOGGER.debug("Finished")
