"""
Unit tests for the rudi_dire_insp.manifests module.
"""

# Core python imports
import copy
import io
import logging

# 3rd party imports
import pytest

# Imports of code-under-test
import rudi_dire_insp.exceptions as my_exceptions
import rudi_dire_insp.hashing as my_hashing
import rudi_dire_insp.manifests as my_manifests

# Module variables
_LOGGER = logging.getLogger(__name__)
pytestmark = pytest.mark.unit


def test_rb_manifest_props():
    """Smoke test the properties of the RawBytesManifest class"""

    # Prepare test data and expected results
    test_data = b'hello world'
    (expected_hashes, expected_size) = my_hashing._HashAlgorithm.calculate_hashes(io.BytesIO(test_data))
    (input_hashes, input_size) = my_hashing._HashAlgorithm.calculate_hashes(io.BytesIO(test_data))
    assert expected_hashes == input_hashes
    assert expected_size == input_size

    # Instantiate the manifest object and verify that its properties return as expected
    manifest = my_manifests.RawBytesManifest(input_hashes, input_size)
    assert expected_hashes == manifest.hashes
    assert id(expected_hashes) != id(manifest.hashes)
    assert expected_size == manifest.size


def test_file_manifest_props():
    """Smoke test the properties of the FileManifest class"""

    # Prepare test data and expected results
    test_data = b'hello world'
    test_data_size = len(test_data)
    expected_raw_manifest = my_manifests.RawBytesManifest(
        my_hashing._HashAlgorithm.calculate_hashes(io.BytesIO(test_data)), test_data_size)
    input_raw_manifest = my_manifests.RawBytesManifest(
        my_hashing._HashAlgorithm.calculate_hashes(io.BytesIO(test_data)), test_data_size)
    assert str(expected_raw_manifest) == str(input_raw_manifest)

    expected_path = ('super_dir', 'sub_dir', 'stuff.txt')
    input_path = copy.deepcopy(expected_path)

    # Instantiate the manifest object and verify that its properties return as expected
    manifest = my_manifests.FileManifest(input_path, input_raw_manifest)
    assert expected_path == manifest.relative_path
    assert str(expected_raw_manifest) == str(manifest.raw_manifest)
