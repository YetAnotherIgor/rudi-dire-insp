"""
Integration tests for _cli module

Note:
      These are partial whilebox tests of key pieces of the cli handling, they are NOT
      a "full end-to-end from the shell" test.
"""

# Core python imports
import codecs
import io
import json
import logging
import typing

# 3rd party imports
import jsonschema
import pytest
import testfixtures

# Imports of code-under-test
import rudi_dire_insp._cli as my_cli
import rudi_dire_insp.core as my_core
import rudi_dire_insp.hashing as my_hashing

# Module variables
_LOGGER = logging.getLogger(__name__)
pytestmark = pytest.mark.integration


def build_test_directory(tmp_directory_posix_path, num_manifests):
    """Populate a test directory and build a an array of expected file manifests for it"""

    root_directory_posix_path = tmp_directory_posix_path / "root-dir"
    root_directory_posix_path.mkdir()
    root_directory_path = str(root_directory_posix_path)

    # Prep inspector and results buffer
    manifests = []
    inspector = my_core._FileInspector(root_dir_path=root_directory_path)

    # Build test files and matching manifests
    for index in range(0, num_manifests + 1):
        # Create the test file
        file_posix_path = root_directory_posix_path / "test-{}.txt".format(index)
        file_posix_path.write_text("hello world {}".format(index))

        # Inspect it and save the manifest
        manifest = inspector.inspect(str(file_posix_path))
        manifests.append(manifest)

    return root_directory_path, manifests


def test_convert_to_json(tmp_path, cli_json_schema):
    """Test the utility function for converting a file manifest into JSON text"""
    _LOGGER.debug("Begin test")

    _, expected_manifests = build_test_directory(tmp_path, num_manifests=1)
    expected_manifest = expected_manifests[0]

    json_text = my_cli._convert_to_json_text(expected_manifest)
    json_data = json.loads(json_text)
    jsonschema.validate(json_data, cli_json_schema)
    assert expected_manifest.relative_path == tuple(json_data['relative_path'])
    assert expected_manifest.raw_manifest.size == json_data['size']
    assert expected_manifest.raw_manifest.hashes == my_hashing.Hashes(**json_data['hashes'])

    _LOGGER.debug("Finished test")


def _translate_to_sorted_json_objects(lines: typing.List[str], json_schema):
    """Translate the text lines into a sorted list of JSON objects"""
    json_objects = []
    for line in lines:
        json_object = json.loads(line)
        jsonschema.validate(json_object, json_schema)
        json_objects.append(json_object)
    sorted_json_objects = sorted(json_objects, key=lambda item: '/'.join(item['relative_path']))
    return sorted_json_objects


def test_run_inspection(tmp_path, cli_json_schema):
    """Test running the inspection"""
    _LOGGER.debug("Begin test")

    # Create the test directory and files
    root_directory_path, expected_manifests = build_test_directory(tmp_path, num_manifests=3)

    # Create the expected JSON output
    expected_text_lines = []
    for expected_manifest in expected_manifests:
        expected_text_lines.append(my_cli._convert_to_json_text(expected_manifest))
    expected_json_objects = _translate_to_sorted_json_objects(expected_text_lines, cli_json_schema)
    _LOGGER.debug("Expecting these json objects: %s", str(expected_json_objects))

    # Run the inspection and capture its output to a buffer
    found_bytes_buffer = io.BytesIO()
    my_cli._run_inspection(root_directory_path, found_bytes_buffer)
    found_bytes = found_bytes_buffer.getvalue()
    found_text = codecs.decode(found_bytes, encoding='utf-8')
    found_text_lines = io.StringIO(found_text).readlines()
    found_json_objects = _translate_to_sorted_json_objects(found_text_lines, cli_json_schema)
    _LOGGER.debug("Found these json objects: %s", str(expected_json_objects))

    # Compare
    testfixtures.compare(expected_json_objects, found_json_objects)

    _LOGGER.debug("Finished test")
