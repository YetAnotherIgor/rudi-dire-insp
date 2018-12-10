"""
Pytest fixtures common to all integration tests.
"""

# Core python imports
import json
import logging
import os

# 3rd party imports
import jsonschema
import pytest

# Module variables
_LOGGER = logging.getLogger(__name__)


@pytest.fixture("session")
def cli_json_schema():
    """Load the JSON schema for each JSON object per
    line in the cli output stream"""

    # Read the JSON document
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    schema_path = os.path.join(data_path, 'output-schema.json')
    _LOGGER.debug("Loading JSON schema for cli output from this file: %s",
                  schema_path)
    with open(schema_path, 'r') as schema_file:
        json_data = json.load(schema_file)

    # Do sanity check to make sure its a valid JSON schema document
    _ = jsonschema.Draft4Validator(schema=json_data)
    return json_data



