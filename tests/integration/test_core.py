"""
Integration tests for core module
"""

# Core python imports
import logging
import os

# 3rd party imports
import pytest
import testfixtures

# Imports of code-under-test
import rudi_dire_insp.exceptions as my_exceptions
import rudi_dire_insp.core as my_core
import rudi_dire_insp.manifests as my_manifests

# Module variables
_LOGGER = logging.getLogger(__name__)
pytestmark = pytest.mark.integration


def test_file(tmp_path):
    """Smoke test file inspection"""
    _LOGGER.debug("Begin test")

    sub_dir_path = tmp_path / "sub-dir"
    sub_dir_path.mkdir()
    file_path = sub_dir_path / "test.txt"
    file_path.write_text("hello world")
    file_path_str = str(file_path)

    _LOGGER.debug("Testing against file at %s", file_path_str)
    assert os.path.exists(file_path_str)

    # do multiple runs of the inspections to make sure the manifests come out the same each time
    last_manifest = None
    for count in range(0, 2):
        _LOGGER.debug("Testing file inspection on %s for the %d th time", str(file_path_str), count)
        inspector = my_core._FileInspector(root_dir_path=str(tmp_path))
        manifest = inspector.inspect(file_path_str)
        assert isinstance(manifest, my_manifests.FileManifest)
        if last_manifest is not None:
            for attr_name in ['relative_path', 'size', 'hashes']:
                testfixtures.compare(getattr(last_manifest, attr_name, None), getattr(manifest, attr_name, None))
        last_manifest = manifest

    _LOGGER.debug("Finished test")


def test_directory(tmp_path):
    """Smoke test directory inspection"""
    _LOGGER.debug("Begin test")
    sub_dir_path = tmp_path / "sub-dir"
    sub_dir_path.mkdir()

    file_names = ["test1.txt", "test2.txt"]
    for file_name in file_names:
        file_path = sub_dir_path / file_name
        file_path.write_text("test data from {}".format(file_name))

    inspector = my_core.DirectoryInspector()
    root_dir_path = str(tmp_path)
    counter = 0
    for manifest in inspector.inspect(root_dir_path):
        _LOGGER.debug("Got this manifest from the directory inspector: %s", str(manifest))
        assert isinstance(manifest, my_manifests.FileManifest)
        counter += 1

    assert counter == len(file_names)

    _LOGGER.debug("Finished test")
